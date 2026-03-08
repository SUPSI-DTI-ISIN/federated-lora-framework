from sse_starlette import ServerSentEvent

from clients.redis.client import redis_client_async as redis_client_async_base
from services.sse.sse_service_interface import SseServiceInterface
from services.sse.sse_service import SseService

def get_custom_ping() -> ServerSentEvent:
    return ServerSentEvent(comment="keep-alive")

def get_sse_service(redis_client_async = redis_client_async_base) -> SseServiceInterface:
    return SseService.get_instance(redis_client_async=redis_client_async)