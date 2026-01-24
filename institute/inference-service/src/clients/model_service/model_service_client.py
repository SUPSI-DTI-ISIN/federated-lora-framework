import requests
from pydantic import ValidationError

from schemas.model import ModelPathDTO
from .model_service_client_interface import ModelServiceClientInterface


class ModelServiceClient(ModelServiceClientInterface):
    __INSTANCE = None

    def __init__(self, model_service_url: str):
        self.__model_service_url = model_service_url

    @classmethod
    def get_instance(cls, model_service_url: str):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(model_service_url=model_service_url)
        return cls.__INSTANCE

    def get_model_path_for_adapter(self, model_key: str, adapter_version: int) -> ModelPathDTO:
        model_path_for_adapter_url: str = f"{self.__model_service_url}/api_model/model/{model_key}/adapters/{adapter_version}"
        try:
            resp = requests.get(model_path_for_adapter_url, headers={"Accept": "application/json"})
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

        data = resp.json()
        try:
            return ModelPathDTO.model_validate(data)
        except ValidationError as e:
            raise RuntimeError(f"Invalid response shape: {e}")