from contextlib import asynccontextmanager
from fastapi import FastAPI

from config import settings
from services.adapter import get_adapter_registry_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    adapter_registry_service = get_adapter_registry_service()
    adapter_registry_service.ensure_init_adapter(model_key=settings.model_key)

    yield