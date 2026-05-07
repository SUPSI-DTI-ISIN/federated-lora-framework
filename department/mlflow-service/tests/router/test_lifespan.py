import pytest
from unittest.mock import MagicMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient


class TestLifespan:
    def test_calls_ensure_init_adapter_on_startup(self):
        mock_svc = MagicMock()

        with patch("router.lifespan.get_adapter_registry_service", return_value=mock_svc), \
             patch("router.lifespan.settings") as mock_settings:
            mock_settings.model_key = "test-model"

            from router.lifespan import lifespan
            with TestClient(FastAPI(lifespan=lifespan)):
                pass

        mock_svc.ensure_init_adapter.assert_called_once_with(model_key="test-model")

    def test_lifespan_is_callable(self):
        from router.lifespan import lifespan
        assert callable(lifespan)

    def test_app_is_reachable_during_lifespan(self):
        mock_svc = MagicMock()

        with patch("router.lifespan.get_adapter_registry_service", return_value=mock_svc), \
             patch("router.lifespan.settings") as mock_settings:
            mock_settings.model_key = "m"

            from router.lifespan import lifespan
            from router.health.routes import router as health_router

            app = FastAPI(lifespan=lifespan)
            app.include_router(health_router)

            with TestClient(app) as client:
                assert client.get("/health/").status_code == 200
