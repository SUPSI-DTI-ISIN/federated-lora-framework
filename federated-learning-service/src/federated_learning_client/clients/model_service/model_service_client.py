import requests
from pydantic import ValidationError

from .model_service_client_interface import ModelServiceClientInterface
from src.federated_learning_client.clients.schemas import ModelPathDTO


class ModelServiceClient(ModelServiceClientInterface):
    _INSTANCE = None

    def __init__(self, model_service_url: str):
        self.__model_service_url = model_service_url

    @classmethod
    def get_instance(cls, model_service_url: str):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls(model_service_url=model_service_url)
        return cls._INSTANCE


    def get_model_path(self, model_key: str) -> ModelPathDTO:
        model_path_url: str = f"{self.__model_service_url}/api_model/model/{model_key}/path"
        try:
            resp = requests.get(model_path_url, headers={"Accept": "application/json"})
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

        data = resp.json()
        try:
            return ModelPathDTO.model_validate(data)
        except ValidationError as e:
            raise RuntimeError(f"Invalid response shape: {e}")