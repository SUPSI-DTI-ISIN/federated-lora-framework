import pytest
from unittest.mock import MagicMock

from clients.celery.celery_client_service import CeleryClientService


@pytest.fixture(autouse=True)
def reset_singleton():
    CeleryClientService._CeleryClientService__INSTANCE = None
    yield
    CeleryClientService._CeleryClientService__INSTANCE = None


class TestGetInstance:
    def test_returns_same_instance(self):
        i1 = CeleryClientService.get_instance(redis_url="redis://localhost:6379")
        i2 = CeleryClientService.get_instance(redis_url="redis://localhost:6379")
        assert i1 is i2

    def test_creates_new_instance_after_reset(self):
        i1 = CeleryClientService.get_instance(redis_url="redis://localhost:6379")
        CeleryClientService._CeleryClientService__INSTANCE = None
        i2 = CeleryClientService.get_instance(redis_url="redis://localhost:6379")
        assert i1 is not i2


class TestGetCeleryClient:
    def test_returns_celery_client(self):
        svc = CeleryClientService.get_instance(redis_url="redis://localhost:6379")
        client = svc.get_celery_client()
        assert client is not None


class TestCeleryClientInit:
    def test_exports_get_celery_client_service(self):
        import clients.celery as cc
        assert "get_celery_client_service" in cc.__all__

    def test_version(self):
        import clients.celery as cc
        assert cc.__version__ == "1.0.0"
