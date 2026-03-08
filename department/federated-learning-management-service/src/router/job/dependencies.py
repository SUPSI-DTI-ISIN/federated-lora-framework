from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette import ServerSentEvent

from config import settings
from database import DatabaseConnector
from clients.redis.client import redis_client_async as redis_client_async_base
from repositories.federated_learning_job import FederatedLearningJobRepositoryInterface, FederatedLearningJobRepository
from services.federated_learning_job import FederatedLearningJobServiceInterface, FederatedLearningJobService
from services.celery import CeleryJobServiceInterface, CeleryJobService

from services.sse import SseServiceInterface, SseService


def get_custom_ping() -> ServerSentEvent:
    return ServerSentEvent(comment="keep-alive")

def get_federated_learning_job_repository(db: AsyncSession = Depends(DatabaseConnector.get_db_session)) -> FederatedLearningJobRepositoryInterface:
    return FederatedLearningJobRepository(db_session=db)

def get_federated_learning_job_service(federated_learning_job_repository: FederatedLearningJobRepositoryInterface = Depends(get_federated_learning_job_repository)) -> FederatedLearningJobServiceInterface:
    return FederatedLearningJobService(federated_learning_job_repository=federated_learning_job_repository)

def get_celery_job_service(flwr_app_base_path: str = settings.flwr_app_base_path, federated_learning_deployment_environment: str = settings.federated_learning_deployment_environment, is_federated_learning_simulation_environment=settings.is_federated_learning_simulation_environment) -> CeleryJobServiceInterface:
    return CeleryJobService.get_instance(flwr_app_base_path=flwr_app_base_path, federated_learning_deployment_environment=federated_learning_deployment_environment, is_federated_learning_simulation_environment=is_federated_learning_simulation_environment)

def get_sse_service(redis_client_async = redis_client_async_base) -> SseServiceInterface:
    return SseService.get_instance(redis_client_async=redis_client_async)