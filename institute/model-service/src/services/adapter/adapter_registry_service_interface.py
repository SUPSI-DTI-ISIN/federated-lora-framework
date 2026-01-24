from abc import ABC, abstractmethod

from schemas.model import AvailableAdaptersDTO


class AdapterRegistryServiceInterface(ABC):
    @abstractmethod
    def get_available_adapters(self, model_key: str) -> AvailableAdaptersDTO:
        raise NotImplementedError