import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient


def _make_lifespan_patches(mock_consumer=None):
    if mock_consumer is None:
        mock_consumer = MagicMock()
        mock_consumer.start_redis_event_consumer = AsyncMock()

    return (
        patch("router.lifespan.DatabaseConnector.init_database_connection"),
        patch("router.lifespan.DatabaseConnector.test_connection", new_callable=AsyncMock),
        patch("router.lifespan.DatabaseConnector.close_connection", new_callable=AsyncMock),
        patch(
            "router.lifespan.get_federated_learning_job_redis_event_consumer",
            return_value=mock_consumer,
        ),
        patch("asyncio.create_task"),
    )


class TestLifespan:
    def test_lifespan_is_callable(self):
        from router.lifespan import lifespan
        assert callable(lifespan)

    def test_initialises_database_on_startup(self):
        patches = _make_lifespan_patches()
        with patches[0] as mock_init, patches[1], patches[2], patches[3], patches[4]:
            from router.lifespan import lifespan
            with TestClient(FastAPI(lifespan=lifespan)):
                pass

        mock_init.assert_called_once()

    def test_tests_connection_on_startup(self):
        patches = _make_lifespan_patches()
        with patches[0], patches[1] as mock_test, patches[2], patches[3], patches[4]:
            from router.lifespan import lifespan
            with TestClient(FastAPI(lifespan=lifespan)):
                pass

        mock_test.assert_awaited_once()

    def test_closes_connection_on_shutdown(self):
        patches = _make_lifespan_patches()
        with patches[0], patches[1], patches[2] as mock_close, patches[3], patches[4]:
            from router.lifespan import lifespan
            with TestClient(FastAPI(lifespan=lifespan)):
                pass

        mock_close.assert_awaited_once()

    def test_starts_redis_event_consumer_task(self):
        patches = _make_lifespan_patches()
        with patches[0], patches[1], patches[2], patches[3], patches[4] as mock_create_task:
            from router.lifespan import lifespan
            with TestClient(FastAPI(lifespan=lifespan)):
                pass

        mock_create_task.assert_called_once()

    def test_app_is_reachable_during_lifespan(self):
        patches = _make_lifespan_patches()
        with patches[0], patches[1], patches[2], patches[3], patches[4]:
            from router.lifespan import lifespan
            from router.health.routes import router as health_router

            app = FastAPI(lifespan=lifespan)
            app.include_router(health_router)

            with TestClient(app) as client:
                assert client.get("/health/").status_code == 200
