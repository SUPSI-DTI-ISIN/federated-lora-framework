from fastapi import APIRouter

from router.health import router as health_router
from router.model_base import router as model_base_router

api_router = APIRouter()

api_router.include_router(router=health_router)
api_router.include_router(router=model_base_router)