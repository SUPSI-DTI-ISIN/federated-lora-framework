import gc

import torch

from typing import Optional
from datetime import datetime, timezone

from transformers import PreTrainedModel, PreTrainedTokenizer, AutoModelForCausalLM, AutoTokenizer
from accelerate.hooks import remove_hook_from_module
from accelerate import dispatch_model, infer_auto_device_map
from accelerate.utils import get_balanced_memory

from clients.model_service import ModelServiceClientInterface
from schemas.exceptions import ModelLoadingError
from schemas.model import LoadedModel
from utils import TorchDtypeUtils, QuantizationUtils
from .model_service_interface import ModelServiceInterface


class ModelService(ModelServiceInterface):
    __INSTANCE = None

    def __init__(self, model_service_client: ModelServiceClientInterface, max_cached_adapters: int, device_map: str):
        self.__model_service_client = model_service_client
        self.__device_map = device_map
        self.__max_cached_adapters = max_cached_adapters

        self.__model_key: Optional[str] = None
        self.__model: Optional[PreTrainedModel] = None
        self.__tokenizer: Optional[PreTrainedTokenizer] = None
        self.__loaded_adapters: dict[int, str] = {}
        self.__adapter_lru: list[int] = []

    @classmethod
    def get_instance(cls, model_service_client: ModelServiceClientInterface, max_cached_adapters: int, device_map: str):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(model_service_client=model_service_client, max_cached_adapters=max_cached_adapters, device_map=device_map)
        return cls.__INSTANCE


    def get_or_load_model(self, model_key: str, adapter_version: Optional[int]) -> LoadedModel:
        self.__ensure_base_model(model_key)

        if self.__model is None or self.__tokenizer is None:
            raise ModelLoadingError(model_key=model_key)

        if adapter_version is None:
            if self.__loaded_adapters:
                self.__model.disable_adapters()
            return LoadedModel(
                model=self.__model,
                tokenizer=self.__tokenizer,
                has_adapter=False,
                loaded_at=datetime.now(timezone.utc),
            )

        self.__ensure_adapter(model_key=model_key, adapter_version=adapter_version)
        self.__activate_adapter(adapter_version)

        return LoadedModel(
            model=self.__model,
            tokenizer=self.__tokenizer,
            has_adapter=True,
            loaded_at=datetime.now(timezone.utc),
        )


    def __ensure_base_model(self, model_key: str):
        if self.__model is not None and self.__model_key == model_key:
            return

        self.__unload_base_model()

        model_paths = self.__model_service_client.get_model_path_for_inference(
            model_key=model_key,
            adapter_version=None,
        )

        self.__model = AutoModelForCausalLM.from_pretrained(
            model_paths.model_base_path,
            device_map=self.__device_map,
            quantization_config=QuantizationUtils.get_quantization_config(),
            dtype=TorchDtypeUtils.get_torch_dtype(),
            use_safetensors=True,
        )
        self.__tokenizer = AutoTokenizer.from_pretrained(model_paths.model_base_path)
        self.__model.eval()
        self.__model_key = model_key


    def __unload_base_model(self):
        if self.__model is None:
            return

        del self.__model
        del self.__tokenizer
        self.__model = None
        self.__tokenizer = None
        self.__model_key = None
        self.__loaded_adapters.clear()
        self.__adapter_lru.clear()
        gc.collect()
        torch.cuda.empty_cache()


    def __ensure_adapter(self, model_key: str, adapter_version: int):
        if adapter_version in self.__loaded_adapters:
            return

        if len(self.__loaded_adapters) >= self.__max_cached_adapters:
            self.__evict_lru_adapter()

        model_paths = self.__model_service_client.get_model_path_for_inference(
            model_key=model_key,
            adapter_version=adapter_version,
        )

        adapter_name = f"v{adapter_version}"
        remove_hook_from_module(self.__model, recurse=True)
        self.__model.load_adapter(model_paths.adapter_path, adapter_name=adapter_name)
        
        max_memory = get_balanced_memory(self.__model)
        device_map = infer_auto_device_map(self.__model, max_memory=max_memory)
        self.__model = dispatch_model(self.__model, device_map=device_map)

        self.__loaded_adapters[adapter_version] = adapter_name
        self.__adapter_lru.append(adapter_version)

    def __activate_adapter(self, adapter_version: int):
        adapter_name = self.__loaded_adapters[adapter_version]
        self.__model.set_adapter(adapter_name)

        self.__adapter_lru.remove(adapter_version)
        self.__adapter_lru.append(adapter_version)

    def __evict_lru_adapter(self):
        if not self.__adapter_lru:
            return

        lru_version = self.__adapter_lru.pop(0)
        adapter_name = self.__loaded_adapters.pop(lru_version)
        self.__model.delete_adapter(adapter_name)