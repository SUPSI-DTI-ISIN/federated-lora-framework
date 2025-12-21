from fastapi import APIRouter

from .documents import router as documents_router
from .health import router as health_router

api_router = APIRouter()

api_router.include_router(router=documents_router)
api_router.include_router(router=health_router)