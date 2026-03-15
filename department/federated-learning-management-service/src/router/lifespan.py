import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import DatabaseConnector
from clients.redis.service import RedisJobEventConsumerInterface, RedisJobEventConsumer
from clients.redis.client import redis_client_async


@asynccontextmanager
async def lifespan(app: FastAPI):
    DatabaseConnector.init_database_connection()

    await DatabaseConnector.test_connection()

    redis_job_event_consumer: RedisJobEventConsumerInterface = RedisJobEventConsumer(
        redis_client_async=redis_client_async,
    )
    asyncio.create_task(redis_job_event_consumer.start())

    yield

    await DatabaseConnector.close_connection()