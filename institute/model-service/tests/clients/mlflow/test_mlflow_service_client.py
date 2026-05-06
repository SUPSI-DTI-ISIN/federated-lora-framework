import pytest
from unittest.mock import patch, MagicMock

from clients.mlflow.mlflow_service_client import MlFlowServiceClient
from clients.schemas import ManifestDTO, ModelAdaptersVersionDTO, FileDTO


@pytest.fixture(autouse=True)
def reset_singleton():
    MlFlowServiceClient._MlFlowServiceClient__INSTANCE = None
    yield
    MlFlowServiceClient._MlFlowServiceClient__INSTANCE = None


def _manifest_data():
    return {"model_key": "llama-3", "files": [{"size": 100, "rel_path": "model.bin", "hash": "abc"}]}


def _adapters_data():
    return {"model_key": "llama-3", "adapters_version": [1, 2]}


class TestGetInstance:
    def test_returns_same_instance(self):
        i1 = MlFlowServiceClient.get_instance(mlflow_department_service_url="http://mlflow:9010")
        i2 = MlFlowServiceClient.get_instance(mlflow_department_service_url="http://mlflow:9010")
        assert i1 is i2

    def test_creates_new_instance_after_reset(self):
        i1 = MlFlowServiceClient.get_instance(mlflow_department_service_url="http://mlflow:9010")
        MlFlowServiceClient._MlFlowServiceClient__INSTANCE = None
        i2 = MlFlowServiceClient.get_instance(mlflow_department_service_url="http://mlflow:9010")
        assert i1 is not i2


class TestGetModelBaseManifest:
    def _client(self):
        return MlFlowServiceClient(mlflow_department_service_url="http://mlflow:9010")

    def test_returns_manifest_dto(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = _manifest_data()

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp):
            result = self._client().get_model_base_manifest(model_key="llama-3")

        assert isinstance(result, ManifestDTO)
        assert result.model_key == "llama-3"
        assert len(result.files) == 1

    def test_raises_runtime_error_on_http_error(self):
        import requests as req
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = req.exceptions.HTTPError("404")

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp):
            with pytest.raises(RuntimeError):
                self._client().get_model_base_manifest(model_key="llama-3")

    def test_raises_runtime_error_on_invalid_response(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {"unexpected": "data"}

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp):
            with pytest.raises(RuntimeError, match="Invalid response shape"):
                self._client().get_model_base_manifest(model_key="llama-3")

    def test_url_contains_model_key_and_manifest(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = _manifest_data()

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp) as mock_get:
            self._client().get_model_base_manifest(model_key="llama-3")

        url = mock_get.call_args[0][0]
        assert "llama-3" in url
        assert "manifest" in url


class TestGetModelFile:
    def _client(self):
        return MlFlowServiceClient(mlflow_department_service_url="http://mlflow:9010")

    def test_returns_response(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp):
            result = self._client().get_model_file(model_key="llama-3", model_file_path="model.bin")

        assert result is mock_resp

    def test_raises_runtime_error_on_http_error(self):
        import requests as req
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = req.exceptions.HTTPError("500")

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp):
            with pytest.raises(RuntimeError):
                self._client().get_model_file(model_key="llama-3", model_file_path="model.bin")

    def test_url_contains_model_key_and_file_path(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp) as mock_get:
            self._client().get_model_file(model_key="llama-3", model_file_path="config.json")

        url = mock_get.call_args[0][0]
        assert "llama-3" in url
        assert "config.json" in url


class TestGetAdaptersVersion:
    def _client(self):
        return MlFlowServiceClient(mlflow_department_service_url="http://mlflow:9010")

    def test_returns_adapters_version_dto(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = _adapters_data()

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp):
            result = self._client().get_adapters_version(model_key="llama-3")

        assert isinstance(result, ModelAdaptersVersionDTO)
        assert result.adapters_version == [1, 2]

    def test_raises_runtime_error_on_http_error(self):
        import requests as req
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = req.exceptions.HTTPError("404")

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp):
            with pytest.raises(RuntimeError):
                self._client().get_adapters_version(model_key="llama-3")

    def test_raises_runtime_error_on_invalid_response(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {"bad": "shape"}

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp):
            with pytest.raises(RuntimeError, match="Invalid response shape"):
                self._client().get_adapters_version(model_key="llama-3")


class TestGetAdapterManifest:
    def _client(self):
        return MlFlowServiceClient(mlflow_department_service_url="http://mlflow:9010")

    def test_returns_manifest_dto(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = _manifest_data()

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp):
            result = self._client().get_adapter_manifest(model_key="llama-3", adapter_version=1)

        assert isinstance(result, ManifestDTO)

    def test_raises_runtime_error_on_http_error(self):
        import requests as req
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = req.exceptions.HTTPError("404")

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp):
            with pytest.raises(RuntimeError):
                self._client().get_adapter_manifest(model_key="llama-3", adapter_version=1)

    def test_raises_runtime_error_on_invalid_response(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {"bad": "shape"}

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp):
            with pytest.raises(RuntimeError, match="Invalid response shape"):
                self._client().get_adapter_manifest(model_key="llama-3", adapter_version=1)

    def test_url_contains_adapter_version(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = _manifest_data()

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp) as mock_get:
            self._client().get_adapter_manifest(model_key="llama-3", adapter_version=2)

        url = mock_get.call_args[0][0]
        assert "adapters/2" in url
        assert "manifest" in url


class TestGetAdapterFile:
    def _client(self):
        return MlFlowServiceClient(mlflow_department_service_url="http://mlflow:9010")

    def test_returns_response(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp):
            result = self._client().get_adapter_file(
                model_key="llama-3", adapter_version=1, model_file_path="adapter.bin"
            )

        assert result is mock_resp

    def test_raises_runtime_error_on_http_error(self):
        import requests as req
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = req.exceptions.HTTPError("500")

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp):
            with pytest.raises(RuntimeError):
                self._client().get_adapter_file(
                    model_key="llama-3", adapter_version=1, model_file_path="adapter.bin"
                )

    def test_url_contains_adapter_version_and_file(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()

        with patch("clients.mlflow.mlflow_service_client.requests.get", return_value=mock_resp) as mock_get:
            self._client().get_adapter_file(
                model_key="llama-3", adapter_version=3, model_file_path="adapter_model.bin"
            )

        url = mock_get.call_args[0][0]
        assert "adapters/3" in url
        assert "adapter_model.bin" in url


class TestMlflowClientInit:
    def test_exports(self):
        import clients.mlflow as cm
        assert "MlFlowServiceClientInterface" in cm.__all__
        assert "get_mlflow_service_client" in cm.__all__

    def test_version(self):
        import clients.mlflow as cm
        assert cm.__version__ == "1.0.0"
