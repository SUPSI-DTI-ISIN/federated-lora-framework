from abc import ABC, abstractmethod
from typing import Optional

from clients.schemas import ModelPathDTO


class ModelServiceClientInterface(ABC):
    @abstractmethod
    def get_model_path_for_inference(self, model_key: str, adapter_version: Optional[int]) -> ModelPathDTO:
        raise NotImplementedError