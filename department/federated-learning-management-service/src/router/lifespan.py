import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import DatabaseConnector
from services.federated_learning_job.redis import get_federated_learning_job_redis_event_consumer

@asynccontextmanager
async def lifespan(app: FastAPI):
    DatabaseConnector.init_database_connection()

    await DatabaseConnector.test_connection()

    federated_learning_job_redis_event_consumer = get_federated_learning_job_redis_event_consumer()
    asyncio.create_task(federated_learning_job_redis_event_consumer.start_redis_event_consumer())

    yield

    await DatabaseConnector.close_connection()