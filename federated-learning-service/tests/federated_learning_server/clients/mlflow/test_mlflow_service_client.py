import pytest
from unittest.mock import patch, MagicMock

from src.federated_learning_server.clients.mlflow.mlflow_service_client import MlFlowServiceClient
from src.federated_learning_server.clients.schemas import FederatedDataDTO


@pytest.fixture(autouse=True)
def reset_singleton():
    MlFlowServiceClient._INSTANCE = None
    yield
    MlFlowServiceClient._INSTANCE = None


class TestGetInstance:
    def test_returns_same_instance(self):
        i1 = MlFlowServiceClient.get_instance(mlflow_service_url="http://mlflow:9010")
        i2 = MlFlowServiceClient.get_instance(mlflow_service_url="http://mlflow:9010")
        assert i1 is i2

    def test_creates_new_instance_after_reset(self):
        i1 = MlFlowServiceClient.get_instance(mlflow_service_url="http://mlflow:9010")
        MlFlowServiceClient._INSTANCE = None
        i2 = MlFlowServiceClient.get_instance(mlflow_service_url="http://mlflow:9010")
        assert i1 is not i2


class TestGetFederatedData:
    def _client(self):
        return MlFlowServiceClient(mlflow_service_url="http://mlflow:9010")

    def test_returns_federated_data_dto(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {
            "new_adapter_path": "/adapters/new",
            "latest_adapter_path": "/adapters/latest",
        }

        with patch("src.federated_learning_server.clients.mlflow.mlflow_service_client.requests.get",
                   return_value=mock_resp):
            result = self._client().get_federated_data(model_key="llama-3")

        assert isinstance(result, FederatedDataDTO)
        assert result.new_adapter_path == "/adapters/new"
        assert result.latest_adapter_path == "/adapters/latest"

    def test_raises_runtime_error_on_http_error(self):
        import requests as req
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = req.exceptions.HTTPError("404")

        with patch("src.federated_learning_server.clients.mlflow.mlflow_service_client.requests.get",
                   return_value=mock_resp):
            with pytest.raises(RuntimeError):
                self._client().get_federated_data(model_key="llama-3")

    def test_raises_runtime_error_on_invalid_response(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {"unexpected": "data"}

        with patch("src.federated_learning_server.clients.mlflow.mlflow_service_client.requests.get",
                   return_value=mock_resp):
            with pytest.raises(RuntimeError, match="Invalid response shape"):
                self._client().get_federated_data(model_key="llama-3")

    def test_url_contains_model_key(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {
            "new_adapter_path": "/adapters/new",
            "latest_adapter_path": "/adapters/latest",
        }

        with patch("src.federated_learning_server.clients.mlflow.mlflow_service_client.requests.get",
                   return_value=mock_resp) as mock_get:
            self._client().get_federated_data(model_key="llama-3")

        url = mock_get.call_args[0][0]
        assert "llama-3" in url
        assert "federated" in url


class TestMlflowClientInit:
    def test_exports(self):
        from src.federated_learning_server.clients.mlflow import __all__
        assert "MlFlowServiceClientInterface" in __all__
        assert "MlFlowServiceClient" in __all__

    def test_version(self):
        from src.federated_learning_server.clients.mlflow import __version__
        assert __version__ == "1.0.0"
