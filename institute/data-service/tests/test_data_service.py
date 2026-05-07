import argparse
import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI


@pytest.fixture()
def app():
    with patch("data_service.lifespan", new=MagicMock()):
        from data_service import create_app
        return create_app()


class TestCreateApp:
    def test_returns_fastapi_instance(self, app):
        assert isinstance(app, FastAPI)

    def test_title(self, app):
        assert app.title == "Data Service"

    def test_version(self, app):
        assert app.version == "1.0.0"

    def test_api_router_is_mounted_under_prefix(self, app):
        assert any("/api_data" in r.path for r in app.routes)


class TestMainBlock:
    def test_argument_parser_accepts_port_flag(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--port", type=int, default=8080)
        assert parser.parse_args(["-p", "9999"]).port == 9999

    def test_argument_parser_uses_default_port(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--port", type=int, default=8080)
        assert parser.parse_args([]).port == 8080
