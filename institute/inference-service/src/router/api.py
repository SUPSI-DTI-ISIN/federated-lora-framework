from fastapi import APIRouter

from router.inference import router as inference_router
from router.health import router as health_router

api_router = APIRouter()

api_router.include_router(router=inference_router)
api_router.include_router(router=health_router)