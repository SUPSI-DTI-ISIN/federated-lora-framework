from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

from clients.mlflow import MlFlowServiceClientInterface, MlFlowServiceClient
from config import settings
from services.utils import InitModelDownloaderServiceInterface, InitModelDownloaderService


@asynccontextmanager
async def lifespan(app: FastAPI):
    mlflow_service_client: MlFlowServiceClientInterface = MlFlowServiceClient.get_instance(department_service_url=settings.department_service_url)

    init_model_downloader_service: InitModelDownloaderServiceInterface = InitModelDownloaderService.get_instance(mlflow_service_client=mlflow_service_client)
    init_model_downloader_service.download_base_model(model_key=settings.model_key)

    yield