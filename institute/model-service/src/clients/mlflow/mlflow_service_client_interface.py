from requests.models import Response
from abc import ABC, abstractmethod

from clients.schemas import ManifestDTO, ModelAdaptersVersionDTO


class MlFlowServiceClientInterface(ABC):
    @abstractmethod
    def get_model_base_manifest(self, model_key: str) -> ManifestDTO:
        raise NotImplementedError

    @abstractmethod
    def get_model_file(self, model_key: str, model_file_path: str) -> Response:
        raise NotImplementedError

    @abstractmethod
    def get_adapters_version(self, model_key: str) -> ModelAdaptersVersionDTO:
        raise NotImplementedError

    @abstractmethod
    def get_adapter_manifest(self, model_key: str, adapter_version: int) -> ManifestDTO:
        raise NotImplementedError

    @abstractmethod
    def get_adapter_file(self, model_key: str, adapter_version: int, model_file_path: str) -> Response:
        raise NotImplementedError