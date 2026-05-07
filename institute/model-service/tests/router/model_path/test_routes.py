import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from schemas.model import ModelPathDTO
from router.model_path.routes import router
from services.model_path import ModelPathServiceInterface, get_model_path_service


def _path_dto(base="/models/llama", adapter=None):
    return ModelPathDTO(model_base_path=base, adapter_path=adapter)


@pytest.fixture()
def mock_service():
    return MagicMock(spec=ModelPathServiceInterface)


@pytest.fixture()
def client(mock_service):
    app = FastAPI()
    app.dependency_overrides[get_model_path_service] = lambda: mock_service
    app.include_router(router)
    return TestClient(app, raise_server_exceptions=False)


class TestGetModelPath:
    def test_returns_200_without_adapter(self, client, mock_service):
        mock_service.get_model_path.return_value = _path_dto()
        response = client.get("/models/llama-3/path")
        assert response.status_code == 200
        assert response.json()["model_base_path"] == "/models/llama"
        assert response.json()["adapter_path"] is None

    def test_returns_200_with_adapter(self, client, mock_service):
        mock_service.get_model_path.return_value = _path_dto(adapter="/models/llama/adapters/v1")
        response = client.get("/models/llama-3/path?adapter_version=1")
        assert response.status_code == 200
        assert response.json()["adapter_path"] == "/models/llama/adapters/v1"

    def test_returns_404_when_path_not_found(self, client, mock_service):
        mock_service.get_model_path.side_effect = FileNotFoundError("Model path does not exist")
        response = client.get("/models/llama-3/path")
        assert response.status_code == 404

    def test_passes_model_key_to_service(self, client, mock_service):
        mock_service.get_model_path.return_value = _path_dto()
        client.get("/models/mistral/path")
        mock_service.get_model_path.assert_called_once_with(
            model_key="mistral", adapter_version=None
        )

    def test_passes_adapter_version_to_service(self, client, mock_service):
        mock_service.get_model_path.return_value = _path_dto(adapter="/adapters/v2")
        client.get("/models/llama-3/path?adapter_version=2")
        mock_service.get_model_path.assert_called_once_with(
            model_key="llama-3", adapter_version=2
        )

    def test_router_init_export(self):
        from router.model_path import router as r
        assert r is not None

    def test_router_version(self):
        import router.model_path as rmp
        assert rmp.__version__ == "1.0.0"
