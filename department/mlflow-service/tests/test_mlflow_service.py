import argparse
import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware


@pytest.fixture()
def app():
    with patch("router.lifespan.get_adapter_registry_service", return_value=MagicMock()), \
         patch("router.lifespan.settings") as mock_settings:
        mock_settings.model_key = "m"
        from mlflow_service import create_app
        return create_app()


class TestCreateApp:
    def test_returns_fastapi_instance(self, app):
        assert isinstance(app, FastAPI)

    def test_title(self, app):
        assert app.title == "MlFlow Service"

    def test_version(self, app):
        assert app.version == "1.0.0"

    def test_gzip_middleware_is_registered(self, app):
        assert GZipMiddleware in [m.cls for m in app.user_middleware]

    def test_api_router_is_mounted_under_api_mlflow_prefix(self, app):
        assert any("/api_mlflow" in r.path for r in app.routes)


class TestMainBlock:
    def test_argument_parser_accepts_port_flag(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--port", type=int, default=9010)
        assert parser.parse_args(["-p", "9999"]).port == 9999

    def test_argument_parser_uses_default_port(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--port", type=int, default=9010)
        assert parser.parse_args([]).port == 9010
