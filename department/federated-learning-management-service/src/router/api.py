from fastapi import APIRouter

from router.health import router as health_router
from router.job import router as job_router

api_router = APIRouter()

api_router.include_router(router=health_router)
api_router.include_router(router=job_router)