from pathlib import Path

from clients.mlflow import MlFlowServiceClientInterface
from commons import ModelPathUtils, FileUtils
from .init_model_downloader_service_interface import InitModelDownloaderServiceInterface
from .model_validity_service import ModelValidityService


class InitModelDownloaderService(InitModelDownloaderServiceInterface):
    _INSTANCE = None

    def __init__(self, mlflow_service_client: MlFlowServiceClientInterface):
        self.__mlflow_service_client = mlflow_service_client

    @classmethod
    def get_instance(cls, mlflow_service_client: MlFlowServiceClientInterface):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls(mlflow_service_client=mlflow_service_client)
        return cls._INSTANCE


    def download_base_model(self, model_key: str) -> None:
        model_manifest = self.__mlflow_service_client.get_model_base_manifest(model_key=model_key)

        target_folder_path = Path(ModelPathUtils.get_model_base_path(model_key=model_key))
        invalid_or_missing_files = FileUtils.check_local_files_validity(target_folder_path=target_folder_path, manifest=model_manifest)

        if len(invalid_or_missing_files) > 0:
            FileUtils.delete_files(target_folder_path=target_folder_path, model_files=invalid_or_missing_files)
            ModelValidityService.fetch_model(mlflow_service_client=self.__mlflow_service_client, model_key=model_key, manifest=model_manifest, files_to_download=invalid_or_missing_files)

        print(f"Model {model_key} loaded successfully at startup." )