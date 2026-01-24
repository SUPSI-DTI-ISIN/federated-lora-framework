from abc import ABC, abstractmethod

from schemas.model import ModelAdaptersVersion, NewAdapterPath


class AdapterRegistryServiceInterface(ABC):
    @abstractmethod
    def get_adapters_version(self, model_key: str) -> ModelAdaptersVersion:
        raise NotImplementedError

    @abstractmethod
    def get_new_adapter_path(self, model_key: str) -> NewAdapterPath:
        raise NotImplementedError