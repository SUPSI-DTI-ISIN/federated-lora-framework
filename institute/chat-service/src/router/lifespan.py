import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from services.inference.redis import get_inference_result_redis_event_consumer
from database import DatabaseConnector

@asynccontextmanager
async def lifespan(app: FastAPI):
    DatabaseConnector.init_database_connection()

    await DatabaseConnector.test_connection()

    inference_result_redis_event_consumer = get_inference_result_redis_event_consumer()
    asyncio.create_task(inference_result_redis_event_consumer.start_redis_event_consumer())

    yield

    await DatabaseConnector.close_connection()