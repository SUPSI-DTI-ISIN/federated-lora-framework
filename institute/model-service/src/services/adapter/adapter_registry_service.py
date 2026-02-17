import os
import shutil
from pathlib import Path
from typing import List

from clients.mlflow import MlFlowServiceClientInterface
from commons import ModelPathUtils, FileUtils
from schemas.model import AvailableAdaptersDTO, AdapterDTO, ModelPathDTO
from .adapter_registry_service_interface import AdapterRegistryServiceInterface
from .adapter_validity_service import AdapterValidityService


class AdapterRegistryService(AdapterRegistryServiceInterface):
    __INSTANCE = None

    def __init__(self, mlflow_service_client: MlFlowServiceClientInterface):
        self.__mlflow_service_client = mlflow_service_client

    @classmethod
    def get_instance(cls, mlflow_service_client: MlFlowServiceClientInterface):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(mlflow_service_client=mlflow_service_client)
        return cls.__INSTANCE


    def get_available_adapters(self, model_key: str) -> AvailableAdaptersDTO:
        adapters_version_from_department_dto = self.__mlflow_service_client.get_adapters_version(model_key=model_key)

        if adapters_version_from_department_dto.adapters_version is None:
            return AvailableAdaptersDTO(model_key=model_key)

        adapters_version_local_path = ModelPathUtils.get_model_adapters_path(model_key=model_key)

        if not os.path.exists(adapters_version_local_path):
            return AvailableAdaptersDTO(
                model_key=model_key,
                adapters=[
                    AdapterDTO(version=int(adapter_version), available_local=False)
                    for adapter_version in adapters_version_from_department_dto.adapters_version
                ]
            )

        adapters_version_local = []
        for entry in os.listdir(adapters_version_local_path):
            version_path = os.path.join(adapters_version_local_path, entry)
            if os.path.isdir(version_path) and entry.isdigit() and os.listdir(version_path):
                adapters_version_local.append(int(entry))

        if not adapters_version_local:
            return AvailableAdaptersDTO(
                model_key=model_key,
                adapters=[
                    AdapterDTO(version=int(adapter_version), available_local=False)
                    for adapter_version in adapters_version_from_department_dto.adapters_version
                ]
            )

        adapters_version_local_set = set(adapters_version_local)

        adapters = [
            AdapterDTO(version=int(adapter_version), available_local=(int(adapter_version) in adapters_version_local_set))
            for adapter_version in adapters_version_from_department_dto.adapters_version
        ]

        local_only_adapters_version = adapters_version_local_set - set(adapters_version_from_department_dto.adapters_version)
        print(f"Local only adapters version {local_only_adapters_version}")
        for local_only_adapter_version in local_only_adapters_version:
            AdapterRegistryService.__delete_adapter_version(model_key=model_key, adapter_version=local_only_adapter_version)

        return AvailableAdaptersDTO(model_key=model_key, adapters=adapters)


    def get_available_local_adapters(self, model_key: str) -> AvailableAdaptersDTO:
        adapters_version_local_path = ModelPathUtils.get_model_adapters_path(model_key=model_key)

        if not os.path.exists(adapters_version_local_path):
            return AvailableAdaptersDTO(
                model_key=model_key
            )

        adapters_version_local = []
        for entry in os.listdir(adapters_version_local_path):
            version_path = os.path.join(adapters_version_local_path, entry)
            if os.path.isdir(version_path) and entry.isdigit() and os.listdir(version_path):
                adapters_version_local.append(int(entry))

        if not adapters_version_local:
            return AvailableAdaptersDTO(
                model_key=model_key,
            )

        return AvailableAdaptersDTO(
            model_key=model_key,
            adapters=[AdapterDTO(version=int(adapter_version), available_local=True) for adapter_version in adapters_version_local]
        )


    def download_remote_adapter(self, model_key: str, adapter_version: int) -> AdapterDTO:
        adapter_manifest = self.__mlflow_service_client.get_adapter_manifest(model_key=model_key, adapter_version=adapter_version)

        target_folder_path = Path(ModelPathUtils.get_model_adapter_path_by_version(model_key=model_key, version=adapter_version))
        invalid_or_missing_files = FileUtils.check_local_files_validity(target_folder_path=target_folder_path, manifest=adapter_manifest)

        if len(invalid_or_missing_files) > 0:
            FileUtils.delete_files(target_folder_path=target_folder_path, model_files=invalid_or_missing_files)
            AdapterValidityService.fetch_adapter(mlflow_service_client=self.__mlflow_service_client, model_key=model_key, adapter_version=adapter_version, manifest=adapter_manifest, files_to_download=invalid_or_missing_files)

        return AdapterDTO(
            version=adapter_version,
            available_local=True
        )

    @staticmethod
    def __delete_adapter_version(model_key: str, adapter_version: int):
        adapter_version_path = Path(
            ModelPathUtils.get_model_adapter_path_by_version(
                model_key=model_key,
                version=adapter_version
            )
        )

        if not adapter_version_path.exists():
            raise FileNotFoundError(f"Model with {model_key} does not have adapter with version {adapter_version}")

        shutil.rmtree(adapter_version_path)