from abc import ABC, abstractmethod
from typing import Optional

from schemas.model import LoadedModel


class ModelServiceInterface(ABC):
    @abstractmethod
    def get_or_load_model(self, model_key: str, adapter_version: Optional[int]) -> LoadedModel:
        raise NotImplementedError