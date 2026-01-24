from fastapi import Depends

from clients.mlflow import MlFlowServiceClientInterface, MlFlowServiceClient
from config import settings
from services.adapter import AdapterRegistryServiceInterface, AdapterRegistryService

def get_mlflow_service_client() -> MlFlowServiceClientInterface:
    return MlFlowServiceClient.get_instance(department_service_url=settings.department_service_url)


def get_adapter_registry_service(mlflow_service_client: MlFlowServiceClientInterface = Depends(get_mlflow_service_client)) -> AdapterRegistryServiceInterface:
    return AdapterRegistryService.get_instance(mlflow_service_client=mlflow_service_client)