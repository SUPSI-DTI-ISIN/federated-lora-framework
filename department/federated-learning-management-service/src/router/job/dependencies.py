from sse_starlette import ServerSentEvent

from clients.redis import redis_client_async as redis_client_async_base
from services.job import JobServiceInterface, JobService

from services.sse import SseServiceInterface, SseService


def get_custom_ping() -> ServerSentEvent:
    return ServerSentEvent(comment="keep-alive")

def get_job_service() -> JobServiceInterface:
    return JobService.get_instance()

def get_sse_service(redis_client_async = redis_client_async_base) -> SseServiceInterface:
    return SseService.get_instance(redis_client_async=redis_client_async)