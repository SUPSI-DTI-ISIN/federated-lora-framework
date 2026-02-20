from fastapi import APIRouter

from router.health import router as health_router
from router.management import router as federated_learning_management_router

api_router = APIRouter()

api_router.include_router(router=health_router)
api_router.include_router(router=federated_learning_management_router)