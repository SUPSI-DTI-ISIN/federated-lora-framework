from abc import ABC, abstractmethod

from schemas.model import ModelPathDTO


class ModelServiceClientInterface(ABC):
    @abstractmethod
    def get_model_path(self) -> ModelPathDTO:
        raise NotImplementedError