from contextlib import asynccontextmanager
from fastapi import FastAPI

from config import settings
from services.utils import InitModelService

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_model_service = InitModelService.get_instance(department_nginx_service_url=settings.department_nginx_service_url)

    init_model_service.download_base_model()

    yield