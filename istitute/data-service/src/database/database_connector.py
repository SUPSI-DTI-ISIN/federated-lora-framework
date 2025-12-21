from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from commons import Environment
from config import settings

class DatabaseConnector:
    _engine = create_async_engine(
        url=settings.database_url,
        echo=settings.environment == Environment.DEV,
        pool_pre_ping=True
    )

    _async_session_local = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    @classmethod
    async def get_db_session(cls):
        async with cls._async_session_local() as session:
            try:
                yield session
            finally:
                await session.close()