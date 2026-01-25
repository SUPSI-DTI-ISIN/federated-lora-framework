from fastapi import APIRouter

from router.health import router as health_router
from router.adapters import router as adapters_router
from router.model_path import router as model_path_router

api_router = APIRouter()

api_router.include_router(router=health_router)
api_router.include_router(router=adapters_router)
api_router.include_router(router=model_path_router)