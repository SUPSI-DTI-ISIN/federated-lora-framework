from contextlib import asynccontextmanager
from fastapi import FastAPI

from clients.mlflow import MlFlowClientProviderInterface, MlFlowClientProvider
from config import settings
from services.utils import InitModelUploaderServiceInterface, InitModelUploaderService


@asynccontextmanager
async def lifespan(app: FastAPI):
    mlflow_client_provider: MlFlowClientProviderInterface = MlFlowClientProvider.get_instance(mlflow_tracking_uri=settings.mlflow_tracking_uri)

    init_model_uploader_service: InitModelUploaderServiceInterface = InitModelUploaderService.get_instance(mlflow_client=mlflow_client_provider.get_mlflow_client())

    init_model_uploader_service.upload_model(model_key=settings.model_key)

    yield