from abc import ABC, abstractmethod
from pathlib import Path

from schemas.model import ManifestDTO


class ModelRegistryServiceInterface(ABC):
    @abstractmethod
    def get_model_manifest(self, model_key: str) -> ManifestDTO:
        raise NotImplementedError

    @abstractmethod
    def get_model_file(self, model_key: str, file_name: str) -> Path:
        raise NotImplementedError

    @abstractmethod
    def get_model_path(self, model_key: str) -> str:
        raise NotImplementedError