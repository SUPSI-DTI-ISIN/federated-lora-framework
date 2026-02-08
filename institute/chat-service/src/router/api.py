from fastapi import APIRouter

from router.chat import router as chat_router
from router.message import router as message_router
from router.health import router as health_router

api_router = APIRouter()

api_router.include_router(router=chat_router)
api_router.include_router(router=message_router)
api_router.include_router(router=health_router)