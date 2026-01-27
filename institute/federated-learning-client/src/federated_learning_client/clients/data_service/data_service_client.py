from typing import List

import requests
from pydantic import ValidationError

from .data_service_client_interface import DataServiceClientInterface
from federated_learning_client.clients.schemas import DocumentDTO


class DataServiceClient(DataServiceClientInterface):
    _INSTANCE = None

    def __init__(self, data_service_url: str):
        self.__data_service_url = data_service_url

    @classmethod
    def get_instance(cls, data_service_url: str):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls(data_service_url=data_service_url)
        return cls._INSTANCE

    def get_documents(self) -> List[DocumentDTO]:
        documents_url: str = f"{self.__data_service_url}/api_data/documents"
        try:
            resp = requests.get(documents_url, headers={"Accept": "application/json"})
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

        data = resp.json()
        try:
            return [DocumentDTO.model_validate(item) for item in data]
        except ValidationError as e:
            raise RuntimeError(f"Invalid response shape: {e}")