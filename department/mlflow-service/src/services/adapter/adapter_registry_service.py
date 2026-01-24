import os
from pathlib import Path

from commons import ModelPathUtils, ManifestUtils, FileUtils
from schemas.model import ModelAdaptersVersionDTO, NewAdapterPathDTO, ManifestDTO
from .adapter_registry_service_interface import AdapterRegistryServiceInterface


class AdapterRegistryService(AdapterRegistryServiceInterface):
    __INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE


    def get_adapters_version(self, model_key: str) -> ModelAdaptersVersionDTO:
        model_adapters_path = ModelPathUtils.get_model_adapters_path(model_key=model_key)

        if not os.path.exists(model_adapters_path):
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


    def get_new_adapter_path(self, model_key: str) -> NewAdapterPathDTO:
        model_adapters_path = ModelPathUtils.get_model_adapters_path(
            model_key=model_key
        )

        if not os.path.exists(model_adapters_path):
            raise FileNotFoundError(f"No adapters found for model '{model_key}'")

        if not os.path.isdir(model_adapters_path):
            return NewAdapterPathDTO(new_adapter_path=os.path.join(model_adapters_path, "1"))

        adapters_versions = self.get_adapters_version(model_key)
        next_version = max(adapters_versions.adapters_version) + 1

        return NewAdapterPathDTO(new_adapter_path=os.path.join(model_adapters_path, str(next_version)))


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