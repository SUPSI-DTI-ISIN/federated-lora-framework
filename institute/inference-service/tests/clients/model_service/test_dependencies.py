import pytest
from clients.model_service.model_service_client import ModelServiceClient
from clients.model_service.dependencies import build_model_service_client


@pytest.fixture(autouse=True)
def reset_singleton():
    ModelServiceClient._ModelServiceClient__INSTANCE = None
    yield
    ModelServiceClient._ModelServiceClient__INSTANCE = None


class TestBuildModelServiceClient:
    def test_returns_model_service_client_instance(self):
        client = build_model_service_client()
        assert isinstance(client, ModelServiceClient)
