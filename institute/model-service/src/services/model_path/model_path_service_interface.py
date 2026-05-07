from abc import ABC, abstractmethod
from typing import Optional

from schemas.model import ModelPathDTO


class ModelPathServiceInterface(ABC):
    @abstractmethod
    def get_model_path(self, model_key: str, adapter_version: Optional[int]) -> ModelPathDTO:
        raise NotImplementedError