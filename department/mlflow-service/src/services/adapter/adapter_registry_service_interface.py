from abc import ABC, abstractmethod

from schemas.model import ModelAdaptersVersionDTO, NewAdapterPathDTO


class AdapterRegistryServiceInterface(ABC):
    @abstractmethod
    def get_adapters_version(self, model_key: str) -> ModelAdaptersVersionDTO:
        raise NotImplementedError

    @abstractmethod
    def get_new_adapter_path(self, model_key: str) -> NewAdapterPathDTO:
        raise NotImplementedError