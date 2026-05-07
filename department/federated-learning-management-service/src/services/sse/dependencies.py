import redis.asyncio
from fastapi import Depends
from sse_starlette import ServerSentEvent

from .sse_service_interface import SseServiceInterface
from .sse_service import SseService

from clients.redis import get_redis_client_async

def get_sse_service(redis_client_async: redis.asyncio.Redis = Depends(get_redis_client_async)) -> SseServiceInterface:
    return SseService.get_instance(redis_client_async=redis_client_async)

def get_custom_ping() -> ServerSentEvent:
    return ServerSentEvent(comment="keep-alive")
