from abc import ABC, abstractmethod

from schemas.model import AvailableAdaptersDTO, AdapterDTO, ModelPathDTO


class AdapterRegistryServiceInterface(ABC):
    @abstractmethod
    def get_available_adapters(self, model_key: str) -> AvailableAdaptersDTO:
        raise NotImplementedError

    @abstractmethod
    def download_remote_adapter(self, model_key: str, adapter_version: int) -> AdapterDTO:
        raise NotImplementedError

    @abstractmethod
    def get_model_path_for_adapter(self, model_key: str, adapter_version: int) -> ModelPathDTO:
        raise NotImplementedError