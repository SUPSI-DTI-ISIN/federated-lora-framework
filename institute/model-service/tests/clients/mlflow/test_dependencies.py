import pytest
from clients.mlflow.mlflow_service_client import MlFlowServiceClient
from clients.mlflow.dependencies import get_mlflow_service_client


@pytest.fixture(autouse=True)
def reset_singleton():
    MlFlowServiceClient._MlFlowServiceClient__INSTANCE = None
    yield
    MlFlowServiceClient._MlFlowServiceClient__INSTANCE = None


class TestGetMlflowServiceClient:
    def test_returns_mlflow_service_client_instance(self):
        client = get_mlflow_service_client()
        assert isinstance(client, MlFlowServiceClient)
