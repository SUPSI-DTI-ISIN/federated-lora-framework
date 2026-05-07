import pytest
from unittest.mock import MagicMock
from services.adapter.adapter_registry_service import AdapterRegistryService
from services.adapter.dependencies import get_adapter_registry_service


@pytest.fixture(autouse=True)
def reset_singleton():
    AdapterRegistryService._AdapterRegistryService__INSTANCE = None
    yield
    AdapterRegistryService._AdapterRegistryService__INSTANCE = None


class TestGetAdapterRegistryService:
    def test_returns_adapter_registry_service_instance(self):
        mock_client = MagicMock()
        svc = get_adapter_registry_service(mlflow_service_client=mock_client)
        assert isinstance(svc, AdapterRegistryService)
