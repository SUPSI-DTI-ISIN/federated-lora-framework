from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from commons import Environment
from config import settings

class DatabaseConnector:
    _engine = None
    _async_session_local = None

    @classmethod
    def init_database_connection(cls):
        cls._engine = create_async_engine(
            url=settings.database_url,
            echo=settings.environment == Environment.DEV,
            pool_pre_ping=True
        )

        cls._async_session_local = async_sessionmaker(
            bind=cls._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @classmethod
    async def test_connection(cls):
        if cls._engine is None:
            raise RuntimeError("Database connector does not initialize connection")

        try:
            async with cls._engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception as e:
            raise e

    @classmethod
    async def close_connection(cls):
        if cls._engine:
            await cls._engine.dispose()
        cls._engine = None
        cls._async_session_local = None

    @classmethod
    async def get_db_session(cls):
        async with cls._async_session_local() as session:
            try:
                yield session
            finally:
                await session.close()