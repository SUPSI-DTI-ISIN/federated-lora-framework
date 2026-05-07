import pytest
from services.model_path.model_path_service import ModelPathService
from services.model_path.dependencies import get_model_path_service


@pytest.fixture(autouse=True)
def reset_singleton():
    ModelPathService._ModelPathService__INSTANCE = None
    yield
    ModelPathService._ModelPathService__INSTANCE = None


class TestGetModelPathService:
    def test_returns_model_path_service_instance(self):
        svc = get_model_path_service()
        assert isinstance(svc, ModelPathService)
