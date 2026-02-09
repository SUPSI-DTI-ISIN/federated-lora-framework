import torch

from typing import Optional
from collections import OrderedDict
from datetime import datetime, timezone

from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

from clients.model_service import ModelServiceClientInterface
from schemas.model import LoadedModel, ModelCacheKey
from .model_service_interface import ModelServiceInterface


class ModelService(ModelServiceInterface):
    __INSTANCE = None

    def __init__(self, model_service_client: ModelServiceClientInterface, max_cached_models: int, device_map: str):
        self.__model_service_client = model_service_client
        self.__max_cached_models = max_cached_models
        self.__device_map = device_map
        self.__model_cache: OrderedDict[ModelCacheKey, LoadedModel] = OrderedDict()

    @classmethod
    def get_instance(cls, model_service_client: ModelServiceClientInterface, max_cached_models: int, device_map: str):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(model_service_client=model_service_client, max_cached_models=max_cached_models, device_map=device_map)
        return cls.__INSTANCE


    def get_or_load_model(self, model_key: str, adapter_version: Optional[int]) -> LoadedModel:
        cache_key = ModelCacheKey(model_key=model_key, adapter_version=adapter_version)

        if cache_key in self.__model_cache:
            self.__model_cache.move_to_end(key=cache_key)
            print("In cache")
            return self.__model_cache[cache_key]

        if len(self.__model_cache) >= self.__max_cached_models:
            self.__evict_least_recently_used()

        print("Not in cache")

        if adapter_version is None:
            loaded_model = self.__load_base_model(model_key=model_key)
        else:
            loaded_model = self.__load_model_with_adapter(model_key=model_key, adapter_version=adapter_version)

        self.__model_cache[cache_key] = loaded_model

        return loaded_model


    def __evict_least_recently_used(self):
        if not self.__model_cache:
            return

        oldest_key, oldest_model = self.__model_cache.popitem(last=False)

        del oldest_model.model
        del oldest_model.tokenizer
        torch.cuda.empty_cache()


    def __load_base_model(self, model_key: str) -> LoadedModel:
        model_paths = self.__model_service_client.get_model_path_for_inference(
            model_key=model_key,
            adapter_version=None
        )

        model = AutoModelForCausalLM.from_pretrained(
            model_paths.model_base_path,
            device_map=self.__device_map,
            torch_dtype=torch.float16,
            use_safetensors=True
        )

        tokenizer = AutoTokenizer.from_pretrained(model_paths.model_base_path)

        return LoadedModel(
            model=model,
            tokenizer=tokenizer,
            has_adapter=False,
            loaded_at=datetime.now(timezone.utc)
        )

    def __load_model_with_adapter(self, model_key: str, adapter_version: int) -> LoadedModel:
        model_paths = self.__model_service_client.get_model_path_for_inference(
            model_key=model_key,
            adapter_version=adapter_version
        )

        base_model = AutoModelForCausalLM.from_pretrained(
            model_paths.model_base_path,
            device_map=self.__device_map,
            torch_dtype=torch.float16,
            use_safetensors=True
        )

        model = PeftModel.from_pretrained(base_model, model_paths.adapter_path)
        tokenizer = AutoTokenizer.from_pretrained(model_paths.adapter_path)

        return LoadedModel(
            model=model,
            tokenizer=tokenizer,
            has_adapter=True,
            loaded_at=datetime.now(timezone.utc)
        )