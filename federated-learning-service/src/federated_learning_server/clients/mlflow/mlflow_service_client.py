import requests
from pydantic import ValidationError

from .mlflow_service_client_interface import MlFlowServiceClientInterface
from src.federated_learning_server.clients.schemas import FederatedDataDTO


class MlFlowServiceClient(MlFlowServiceClientInterface):
    _INSTANCE = None

    def __init__(self, mlflow_service_url: str):
        self.__mlflow_service_url = mlflow_service_url

    @classmethod
    def get_instance(cls, mlflow_service_url: str):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls(mlflow_service_url=mlflow_service_url)
        return cls._INSTANCE

    def get_federated_data(self, model_key: str) -> FederatedDataDTO:
        federated_data_url: str = f"{self.__mlflow_service_url}/api_mlflow/federated/{model_key}"
        try:
            resp = requests.get(federated_data_url, headers={"Accept": "application/json"})
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

        data = resp.json()
        try:
            return FederatedDataDTO.model_validate(data)
        except ValidationError as e:
            raise RuntimeError(f"Invalid response shape: {e}")