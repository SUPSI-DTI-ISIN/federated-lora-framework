import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestLifespan:
    async def test_initializes_database_connection(self):
        from router.lifespan import lifespan
        from fastapi import FastAPI

        app = FastAPI()

        with patch("router.lifespan.DatabaseConnector") as mock_db, \
             patch("router.lifespan.get_inference_result_redis_event_consumer") as mock_consumer, \
             patch("router.lifespan.asyncio.create_task") as mock_task:
            mock_db.init_database_connection = MagicMock()
            mock_db.test_connection = AsyncMock()
            mock_db.close_connection = AsyncMock()
            mock_consumer.return_value = MagicMock(start_redis_event_consumer=AsyncMock())

            async with lifespan(app):
                pass

            mock_db.init_database_connection.assert_called_once()
            mock_db.test_connection.assert_awaited_once()
            mock_db.close_connection.assert_awaited_once()

    async def test_starts_redis_event_consumer(self):
        from router.lifespan import lifespan
        from fastapi import FastAPI

        app = FastAPI()

        with patch("router.lifespan.DatabaseConnector") as mock_db, \
             patch("router.lifespan.get_inference_result_redis_event_consumer") as mock_consumer, \
             patch("router.lifespan.asyncio.create_task") as mock_task:
            mock_db.init_database_connection = MagicMock()
            mock_db.test_connection = AsyncMock()
            mock_db.close_connection = AsyncMock()
            consumer_instance = MagicMock(start_redis_event_consumer=AsyncMock())
            mock_consumer.return_value = consumer_instance

            async with lifespan(app):
                pass

            mock_consumer.assert_called_once()
            mock_task.assert_called_once()
