from abc import ABC, abstractmethod

from schemas.model import ModelPathDTO


class ModelServiceClientInterface(ABC):
    @abstractmethod
    def get_model_path_for_adapter(self, model_key: str, adapter_version: int) -> ModelPathDTO:
        raise NotImplementedError