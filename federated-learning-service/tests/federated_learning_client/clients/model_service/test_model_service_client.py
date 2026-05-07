import pytest
from unittest.mock import patch, MagicMock

from src.federated_learning_client.clients.model_service.model_service_client import ModelServiceClient
from src.federated_learning_client.clients.schemas import ModelPathDTO


@pytest.fixture(autouse=True)
def reset_singleton():
    ModelServiceClient._INSTANCE = None
    yield
    ModelServiceClient._INSTANCE = None


class TestGetInstance:
    def test_returns_same_instance(self):
        i1 = ModelServiceClient.get_instance(model_service_url="http://model:8090")
        i2 = ModelServiceClient.get_instance(model_service_url="http://model:8090")
        assert i1 is i2

    def test_creates_new_instance_after_reset(self):
        i1 = ModelServiceClient.get_instance(model_service_url="http://model:8090")
        ModelServiceClient._INSTANCE = None
        i2 = ModelServiceClient.get_instance(model_service_url="http://model:8090")
        assert i1 is not i2


class TestGetModelPath:
    def _client(self):
        return ModelServiceClient(model_service_url="http://model:8090")

    def test_returns_model_path_dto(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {"model_base_path": "/models/llama", "adapter_path": None}

        with patch("src.federated_learning_client.clients.model_service.model_service_client.requests.get",
                   return_value=mock_resp):
            result = self._client().get_model_path(model_key="llama-3")

        assert isinstance(result, ModelPathDTO)
        assert result.model_base_path == "/models/llama"
        assert result.adapter_path is None

    def test_raises_runtime_error_on_http_error(self):
        import requests as req
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = req.exceptions.HTTPError("404")

        with patch("src.federated_learning_client.clients.model_service.model_service_client.requests.get",
                   return_value=mock_resp):
            with pytest.raises(RuntimeError):
                self._client().get_model_path(model_key="llama-3")

    def test_raises_runtime_error_on_invalid_response(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {"unexpected": "data"}

        with patch("src.federated_learning_client.clients.model_service.model_service_client.requests.get",
                   return_value=mock_resp):
            with pytest.raises(RuntimeError, match="Invalid response shape"):
                self._client().get_model_path(model_key="llama-3")

    def test_url_contains_model_key_and_path(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {"model_base_path": "/models/llama", "adapter_path": None}

        with patch("src.federated_learning_client.clients.model_service.model_service_client.requests.get",
                   return_value=mock_resp) as mock_get:
            self._client().get_model_path(model_key="llama-3")

        url = mock_get.call_args[0][0]
        assert "llama-3" in url
        assert "path" in url
