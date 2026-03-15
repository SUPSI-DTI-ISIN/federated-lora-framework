from fastapi import Depends
from sse_starlette import ServerSentEvent

from clients.redis.client import redis_client_async as redis_client_async_base
from repositories.message import MessageRepositoryInterface
from services.sse import SseServiceInterface, SseService
from router.message.dependencies import get_message_repository

def get_custom_ping() -> ServerSentEvent:
    return ServerSentEvent(comment="keep-alive")

def get_sse_service(message_repository: MessageRepositoryInterface = Depends(get_message_repository)) -> SseServiceInterface:
    return SseService.get_instance(redis_client_async=redis_client_async_base, message_repository=message_repository)