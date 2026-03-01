from sse_starlette import ServerSentEvent

from clients.redis import redis_client_async as redis_client_async_base
from config import settings
from services.job import JobServiceInterface, JobService

from services.sse import SseServiceInterface, SseService


def get_custom_ping() -> ServerSentEvent:
    return ServerSentEvent(comment="keep-alive")

def get_job_service(flwr_app_base_path: str = settings.flwr_app_base_path, federated_learning_deployment_environment: str = settings.federated_learning_deployment_environment, is_federated_learning_simulation_environment=settings.is_federated_learning_simulation_environment) -> JobServiceInterface:
    return JobService.get_instance(flwr_app_base_path=flwr_app_base_path, federated_learning_deployment_environment=federated_learning_deployment_environment, is_federated_learning_simulation_environment=is_federated_learning_simulation_environment)

def get_sse_service(redis_client_async = redis_client_async_base) -> SseServiceInterface:
    return SseService.get_instance(redis_client_async=redis_client_async)