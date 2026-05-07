from .database_connector import DatabaseConnector

async def get_db_session():
    async for session in DatabaseConnector.get_db_session():
        yield session