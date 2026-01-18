from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import DatabaseConnector

@asynccontextmanager
async def lifespan(app: FastAPI):
    DatabaseConnector.init_database_connection()

    await DatabaseConnector.test_connection()

    yield

    await DatabaseConnector.close_connection()