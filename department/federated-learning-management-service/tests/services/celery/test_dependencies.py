import pytest

from services.celery.dependencies import get_celery_job_service
from services.celery.celery_job_service_interface import CeleryJobServiceInterface
from services.celery.celery_job_service import CeleryJobService


@pytest.fixture(autouse=True)
def reset_singleton():
    CeleryJobService._CeleryJobService__INSTANCE = None
    yield
    CeleryJobService._CeleryJobService__INSTANCE = None


class TestGetCeleryJobService:
    def test_returns_celery_job_service_interface(self):
        assert isinstance(get_celery_job_service(), CeleryJobServiceInterface)

    def test_returns_singleton(self):
        assert get_celery_job_service() is get_celery_job_service()

    def test_celery_init_exports(self):
        from services.celery import CeleryJobServiceInterface, get_celery_job_service as fn
        assert CeleryJobServiceInterface is not None
        assert fn is not None

    def test_celery_init_version(self):
        import services.celery as sc
        assert sc.__version__ == "1.0.0"
