from requests.models import Response
from abc import ABC, abstractmethod

from schemas.model import ModelManifestDTO


class MlFlowServiceClientInterface(ABC):
    @abstractmethod
    def get_model_base_manifest(self, model_key: str) -> ModelManifestDTO:
        raise NotImplementedError

    @abstractmethod
    def get_model_file(self, model_key: str, model_file_path: str) -> Response:
        raise NotImplementedError