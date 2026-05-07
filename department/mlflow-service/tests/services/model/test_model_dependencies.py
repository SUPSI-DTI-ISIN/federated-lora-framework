import pytest
from services.model.dependencies import get_model_registry_service
from services.model.model_registry_service_interface import ModelRegistryServiceInterface


@pytest.fixture(autouse=True)
def reset_singleton():
    from services.model.model_registry_service import ModelRegistryService
    ModelRegistryService._ModelRegistryService__INSTANCE = None
    yield
    ModelRegistryService._ModelRegistryService__INSTANCE = None


class TestGetModelRegistryService:
    def test_returns_model_registry_service_interface(self):
        assert isinstance(get_model_registry_service(), ModelRegistryServiceInterface)

    def test_returns_singleton(self):
        assert get_model_registry_service() is get_model_registry_service()

    def test_model_init_exports(self):
        from services.model import ModelRegistryServiceInterface, get_model_registry_service as fn
        assert ModelRegistryServiceInterface is not None
        assert fn is not None

    def test_model_init_version(self):
        import services.model as sm
        assert sm.__version__ == "1.0.0"
