from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from schemas.model import ModelAdaptersVersionDTO, ManifestDTO


class AdapterRegistryServiceInterface(ABC):
    @abstractmethod
    def get_adapters_version(self, model_key: str) -> ModelAdaptersVersionDTO:
        raise NotImplementedError

    @abstractmethod
    def get_new_adapter_path(self, model_key: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_latest_adapter_path(self, model_key: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def get_adapter_manifest(self, model_key: str, adapter_version: int) -> ManifestDTO:
        raise NotImplementedError

    @abstractmethod
    def get_adapter_file(self, model_key: str, adapter_version: int, file_name: str) -> Path:
        raise NotImplementedError