from contextlib import asynccontextmanager
from fastapi import FastAPI

from config import settings
from services.utils import InitModelDownloaderServiceInterface, build_init_model_downloader_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_model_downloader_service: InitModelDownloaderServiceInterface = build_init_model_downloader_service()
    init_model_downloader_service.download_base_model(model_key=settings.model_key)

    yield