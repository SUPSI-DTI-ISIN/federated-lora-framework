import pytest
from unittest.mock import patch, MagicMock

from clients.model_service.model_service_client import ModelServiceClient
from clients.schemas import ModelPathDTO


@pytest.fixture(autouse=True)
def reset_singleton():
    ModelServiceClient._ModelServiceClient__INSTANCE = None
    yield
    ModelServiceClient._ModelServiceClient__INSTANCE = None


class TestGetInstance:
    def test_returns_same_instance(self):
        i1 = ModelServiceClient.get_instance(model_service_url="http://model:8090")
        i2 = ModelServiceClient.get_instance(model_service_url="http://model:8090")
        assert i1 is i2

    def test_creates_new_instance_after_reset(self):
        i1 = ModelServiceClient.get_instance(model_service_url="http://model:8090")
        ModelServiceClient._ModelServiceClient__INSTANCE = None
        i2 = ModelServiceClient.get_instance(model_service_url="http://model:8090")
        assert i1 is not i2


class TestGetModelPathForInference:
    def test_returns_model_path_dto_without_adapter(self):
        client = ModelServiceClient(model_service_url="http://model:8090")
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {
            "model_base_path": "/models/llama",
            "adapter_path": None,
        }

        with patch("clients.model_service.model_service_client.requests.get", return_value=mock_resp):
            result = client.get_model_path_for_inference(model_key="llama-3", adapter_version=None)

        assert isinstance(result, ModelPathDTO)
        assert result.model_base_path == "/models/llama"
        assert result.adapter_path is None

    def test_returns_model_path_dto_with_adapter(self):
        client = ModelServiceClient(model_service_url="http://model:8090")
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {
            "model_base_path": "/models/llama",
            "adapter_path": "/models/llama/adapters/v2",
        }

        with patch("clients.model_service.model_service_client.requests.get", return_value=mock_resp):
            result = client.get_model_path_for_inference(model_key="llama-3", adapter_version=2)

        assert result.adapter_path == "/models/llama/adapters/v2"

    def test_raises_runtime_error_on_http_error(self):
        import requests as req
        client = ModelServiceClient(model_service_url="http://model:8090")
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = req.exceptions.HTTPError("404")

        with patch("clients.model_service.model_service_client.requests.get", return_value=mock_resp):
            with pytest.raises(RuntimeError):
                client.get_model_path_for_inference(model_key="llama-3", adapter_version=None)

    def test_raises_runtime_error_on_invalid_response_shape(self):
        client = ModelServiceClient(model_service_url="http://model:8090")
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {"unexpected_field": "value"}

        with patch("clients.model_service.model_service_client.requests.get", return_value=mock_resp):
            with pytest.raises(RuntimeError, match="Invalid response shape"):
                client.get_model_path_for_inference(model_key="llama-3", adapter_version=None)

    def test_url_includes_adapter_version_param(self):
        client = ModelServiceClient(model_service_url="http://model:8090")
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {
            "model_base_path": "/models/llama",
            "adapter_path": "/adapters/v3",
        }

        with patch("clients.model_service.model_service_client.requests.get", return_value=mock_resp) as mock_get:
            client.get_model_path_for_inference(model_key="llama-3", adapter_version=3)

        called_url = mock_get.call_args[0][0]
        assert "adapter_version=3" in called_url

    def test_url_has_no_params_when_no_adapter(self):
        client = ModelServiceClient(model_service_url="http://model:8090")
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {
            "model_base_path": "/models/llama",
            "adapter_path": None,
        }

        with patch("clients.model_service.model_service_client.requests.get", return_value=mock_resp) as mock_get:
            client.get_model_path_for_inference(model_key="llama-3", adapter_version=None)

        called_url = mock_get.call_args[0][0]
        assert "?" not in called_url


class TestModelServiceClientInit:
    def test_exports(self):
        import clients.model_service as cms
        assert "ModelServiceClientInterface" in cms.__all__
        assert "build_model_service_client" in cms.__all__
