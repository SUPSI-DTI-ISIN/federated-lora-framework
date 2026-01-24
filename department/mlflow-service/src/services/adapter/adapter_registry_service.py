import os

from commons import ModelPathUtils
from schemas.model import ModelAdaptersVersion, NewAdapterPath
from .adapter_registry_service_interface import AdapterRegistryServiceInterface


class AdapterRegistryService(AdapterRegistryServiceInterface):
    __INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE


    def get_adapters_version(self, model_key: str) -> ModelAdaptersVersion:
        model_adapters_path = ModelPathUtils.get_model_adapters_path(model_key=model_key)

        if not os.path.exists(model_adapters_path):
            raise FileNotFoundError(f"No adapters found for model '{model_key}'")

        versions = []
        for entry in os.listdir(model_adapters_path):
            version_path = os.path.join(model_adapters_path, entry)
            if os.path.isdir(version_path) and entry.isdigit() and os.listdir(version_path):
                versions.append(int(entry))

        if not versions:
            raise FileNotFoundError(f"No adapters found for model '{model_key}'")

        versions.sort()

        return ModelAdaptersVersion(
            model_key=model_key,
            adapters_version=versions
        )


    def get_new_adapter_path(self, model_key: str) -> NewAdapterPath:
        model_adapters_path = ModelPathUtils.get_model_adapters_path(
            model_key=model_key
        )

        if not os.path.exists(model_adapters_path):
            raise FileNotFoundError(f"No adapters found for model '{model_key}'")

        if not os.path.isdir(model_adapters_path):
            return NewAdapterPath(new_adapter_path=os.path.join(model_adapters_path, "1"))

        adapters_versions = self.get_adapters_version(model_key)
        next_version = max(adapters_versions.adapters_version) + 1

        return NewAdapterPath(new_adapter_path=os.path.join(model_adapters_path, str(next_version)))