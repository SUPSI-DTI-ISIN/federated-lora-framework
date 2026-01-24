from fastapi import APIRouter

from router.health import router as health_router
from router.model import adapter_router, base_router

api_router = APIRouter()

api_router.include_router(router=health_router)
api_router.include_router(router=adapter_router)
api_router.include_router(router=base_router)