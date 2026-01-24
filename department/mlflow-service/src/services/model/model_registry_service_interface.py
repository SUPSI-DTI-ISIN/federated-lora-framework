from abc import ABC, abstractmethod
from pathlib import Path

from schemas.model import ModelManifestDTO


class ModelRegistryServiceInterface(ABC):
    @abstractmethod
    def get_model_manifest(self, model_key: str) -> ModelManifestDTO:
        raise NotImplementedError

    @abstractmethod
    def get_model_file(self, model_key: str, file_name: str) -> Path:
        raise NotImplementedError