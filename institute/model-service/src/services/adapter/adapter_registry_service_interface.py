from abc import ABC, abstractmethod

from schemas.model import AvailableAdaptersDTO, AdapterDTO


class AdapterRegistryServiceInterface(ABC):
    @abstractmethod
    def get_available_adapters(self, model_key: str) -> AvailableAdaptersDTO:
        raise NotImplementedError

    @abstractmethod
    def get_available_local_adapters(self, model_key: str) -> AvailableAdaptersDTO:
        raise NotImplementedError

    @abstractmethod
    def download_remote_adapter(self, model_key: str, adapter_version: int) -> AdapterDTO:
        raise NotImplementedError