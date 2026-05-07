from fastapi import APIRouter

from router.institutes import router as institute_router
from router.health import router as health_router

api_router = APIRouter()

api_router.include_router(router=institute_router)
api_router.include_router(router=health_router)