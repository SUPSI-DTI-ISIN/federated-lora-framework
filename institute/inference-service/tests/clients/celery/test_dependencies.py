import pytest
from clients.celery.celery_client_service import CeleryClientService
from clients.celery.dependencies import get_celery_client_service


@pytest.fixture(autouse=True)
def reset_singleton():
    CeleryClientService._CeleryClientService__INSTANCE = None
    yield
    CeleryClientService._CeleryClientService__INSTANCE = None


class TestGetCeleryClientService:
    def test_returns_celery_client_service_instance(self):
        svc = get_celery_client_service()
        assert isinstance(svc, CeleryClientService)
