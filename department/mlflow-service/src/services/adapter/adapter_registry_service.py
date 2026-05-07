import shutil
import torch
import gc
import os

from pathlib import Path
from peft import LoraConfig
from accelerate.hooks import remove_hook_from_module

from commons import ModelPathUtils, ManifestUtils, FileUtils, AdapterUtils, ModelUtils
from schemas.model import ModelAdaptersVersionDTO, ManifestDTO
from .adapter_registry_service_interface import AdapterRegistryServiceInterface


class AdapterRegistryService(AdapterRegistryServiceInterface):
    __INSTANCE = None

    def __init__(self, device_map: str, lora_config: LoraConfig):
        self.__device_map = device_map
        self.__lora_config = lora_config

    @classmethod
    def get_instance(cls, device_map: str, lora_config: LoraConfig):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(device_map=device_map, lora_config=lora_config)
        return cls.__INSTANCE

    def ensure_init_adapter(self, model_key: str) -> None:
        init_adapter_path = Path(ModelPathUtils.get_model_init_adapter_path(model_key=model_key))

        if AdapterUtils.is_valid_adapter(path=init_adapter_path):
            return

        model_base_path = ModelPathUtils.get_model_base_path(model_key=model_key)

        base_model = ModelUtils.load_model(model_path=model_base_path, device_map=self.__device_map)
        peft_model = ModelUtils.get_peft_model(model=base_model, lora_config=self.__lora_config)

        init_adapter_path.mkdir(parents=True, exist_ok=True)
        peft_model.save_pretrained(str(init_adapter_path))

        remove_hook_from_module(peft_model, recurse=True)

        peft_model.cpu()
        base_model.cpu()

        del peft_model, base_model

        gc.collect()
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

    def get_adapters_version(self, model_key: str) -> ModelAdaptersVersionDTO:
        model_adapters_path = ModelPathUtils.get_model_adapters_path(model_key=model_key)

        if not Path(model_adapters_path).exists():
            return ModelAdaptersVersionDTO(
                model_key=model_key
            )

        versions = []
        for entry in os.listdir(model_adapters_path):
            version_path = os.path.join(model_adapters_path, entry)
            if os.path.isdir(version_path) and entry.isdigit() and os.listdir(version_path):
                versions.append(int(entry))

        if not versions:
            return ModelAdaptersVersionDTO(
                model_key=model_key
            )

        versions.sort()

        return ModelAdaptersVersionDTO(
            model_key=model_key,
            adapters_version=versions
        )

    def get_new_adapter_path(self, model_key: str) -> str:
        model_adapters_path = ModelPathUtils.get_model_adapters_path(
            model_key=model_key
        )

        if not os.path.exists(model_adapters_path):
            return str(Path(ModelPathUtils.get_model_adapter_path_by_version(model_key=model_key, version=1)).resolve())

        adapters_versions = self.get_adapters_version(model_key)
        if adapters_versions.adapters_version is None:
            return str(Path(ModelPathUtils.get_model_adapter_path_by_version(model_key=model_key, version=1)).resolve())

        next_version = max(adapters_versions.adapters_version) + 1

        return str(Path(ModelPathUtils.get_model_adapter_path_by_version(model_key=model_key, version=next_version)).resolve())

    def get_latest_adapter_path(self, model_key: str) -> str:
        adapters_versions = self.get_adapters_version(model_key)
        if adapters_versions.adapters_version is None:
            return str(Path(ModelPathUtils.get_model_init_adapter_path(model_key=model_key)).resolve())

        latest_version = max(adapters_versions.adapters_version)

        return str(Path(ModelPathUtils.get_model_adapter_path_by_version(model_key=model_key, version=latest_version)).resolve())

    def get_adapter_manifest(self, model_key: str, adapter_version: int) -> ManifestDTO:
        adapter_version_path = ModelPathUtils.get_model_adapter_path_by_version(model_key=model_key, version=adapter_version)

        if not Path(adapter_version_path).exists():
            raise FileNotFoundError(f"Model with {model_key} does not have adapter with version {adapter_version}")

        return ManifestUtils.get_manifest(base_path=Path(adapter_version_path), model_key=model_key)


    def get_adapter_file(self, model_key: str, adapter_version: int, file_name: str) -> Path:
        adapter_version_path = ModelPathUtils.get_model_adapter_path_by_version(model_key=model_key, version=adapter_version)

        if not Path(adapter_version_path).exists():
            raise FileNotFoundError(f"Model with {model_key} does not have adapter with version {adapter_version}")

        return FileUtils.join_paths(base_path=Path(adapter_version_path), file_name=file_name)


    def delete_adapter_version(self, model_key: str, adapter_version: int):
        adapter_version_path = Path(
            ModelPathUtils.get_model_adapter_path_by_version(
                model_key=model_key,
                version=adapter_version
            )
        )

        if not adapter_version_path.exists():
            raise FileNotFoundError(f"Model with {model_key} does not have adapter with version {adapter_version}")

        shutil.rmtree(adapter_version_path)