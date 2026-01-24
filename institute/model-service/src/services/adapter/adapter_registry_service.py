import os
from typing import List

from clients.mlflow import MlFlowServiceClientInterface
from commons import ModelPathUtils
from schemas.model import AvailableAdaptersDTO, AdapterDTO
from .adapter_registry_service_interface import AdapterRegistryServiceInterface


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

        return AvailableAdaptersDTO(model_key=model_key, adapters=adapters)