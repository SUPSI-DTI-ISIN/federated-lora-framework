import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import DatabaseConnector
from clients.redis.service import RedisJobEventConsumerInterface, RedisJobEventConsumer
from clients.redis.client import redis_client_async
from repositories.federated_learning_job import FederatedLearningJobRepositoryInterface, FederatedLearningJobRepository
from services.federated_learning_job import FederatedLearningJobServiceInterface, FederatedLearningJobService


@asynccontextmanager
async def lifespan(app: FastAPI):
    DatabaseConnector.init_database_connection()

    await DatabaseConnector.test_connection()

    async for session in DatabaseConnector.get_db_session():
        federated_learning_job_repository: FederatedLearningJobRepositoryInterface = FederatedLearningJobRepository(db_session=session)
        federated_learning_job_service: FederatedLearningJobServiceInterface = FederatedLearningJobService(federated_learning_job_repository=federated_learning_job_repository)
        redis_job_event_consumer: RedisJobEventConsumerInterface = RedisJobEventConsumer(redis_client_async=redis_client_async, federated_learning_job_service=federated_learning_job_service)
        asyncio.create_task(redis_job_event_consumer.start())

    yield

    await DatabaseConnector.close_connection()