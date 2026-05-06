import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestLifespan:
    async def test_initializes_and_closes_database(self):
        from router.lifespan import lifespan
        from fastapi import FastAPI

        app = FastAPI()

        with patch("router.lifespan.DatabaseConnector") as mock_db:
            mock_db.init_database_connection = MagicMock()
            mock_db.test_connection = AsyncMock()
            mock_db.close_connection = AsyncMock()

            async with lifespan(app):
                pass

            mock_db.init_database_connection.assert_called_once()
            mock_db.test_connection.assert_awaited_once()
            mock_db.close_connection.assert_awaited_once()
