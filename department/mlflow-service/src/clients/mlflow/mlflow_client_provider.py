import mlflow
from mlflow.tracking import MlflowClient

from .mlflow_client_provider_interface import MlFlowClientProviderInterface


class MlFlowClientProvider(MlFlowClientProviderInterface):
    __INSTANCE = None

    def __init__(self, mlflow_tracking_uri: str):
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        self.__client: MlflowClient = MlflowClient()

    @classmethod
    def get_instance(cls, mlflow_tracking_uri: str):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(mlflow_tracking_uri=mlflow_tracking_uri)
        return cls.__INSTANCE

    def get_mlflow_client(self) -> MlflowClient:
        return self.__client