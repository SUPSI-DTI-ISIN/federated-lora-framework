import mlflow
from mlflow.tracking.client import MlflowClient

from commons import ModelPathUtils
from .init_model_uploader_service_interface import InitModelUploaderServiceInterface


class InitModelUploaderService(InitModelUploaderServiceInterface):
    __INSTANCE = None

    def __init__(self, mlflow_client: MlflowClient):
        self.__mlflow_client = mlflow_client

    @classmethod
    def get_instance(cls, mlflow_client: MlflowClient):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(mlflow_client=mlflow_client)
        return cls.__INSTANCE


    def upload_model(self, model_key: str):
        model_path = ModelPathUtils.get_model_base_path(model_key=model_key)
        print(f"Model Path: {model_path}")