import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from schemas.model import AvailableAdaptersDTO, AdapterDTO
from router.adapters.routes import router
from services.adapter import AdapterRegistryServiceInterface, get_adapter_registry_service
from auth import jwt_validator


def _available(model_key="llama-3", adapters=None):
    return AvailableAdaptersDTO(model_key=model_key, adapters=adapters)


def _adapter(version=1, available_local=True):
    return AdapterDTO(version=version, available_local=available_local)


@pytest.fixture()
def mock_service():
    return MagicMock(spec=AdapterRegistryServiceInterface)


@pytest.fixture()
def client(mock_service):
    app = FastAPI()
    app.dependency_overrides[jwt_validator.get_current_user_required] = lambda: MagicMock()
    app.dependency_overrides[get_adapter_registry_service] = lambda: mock_service
    app.include_router(router)
    return TestClient(app, raise_server_exceptions=False)


class TestGetAvailableAdapters:
    def test_returns_200_with_adapters(self, client, mock_service):
        mock_service.get_available_adapters.return_value = _available(
            adapters=[_adapter(1, True), _adapter(2, False)]
        )
        response = client.get("/models/llama-3/adapters")
        assert response.status_code == 200
        assert response.json()["model_key"] == "llama-3"
        assert len(response.json()["adapters"]) == 2

    def test_returns_200_with_no_adapters(self, client, mock_service):
        mock_service.get_available_adapters.return_value = _available()
        response = client.get("/models/llama-3/adapters")
        assert response.status_code == 200
        assert response.json()["adapters"] is None

    def test_passes_model_key_to_service(self, client, mock_service):
        mock_service.get_available_adapters.return_value = _available(model_key="mistral")
        client.get("/models/mistral/adapters")
        mock_service.get_available_adapters.assert_called_once_with(model_key="mistral")


class TestGetAvailableLocalAdapters:
    def test_returns_200_with_local_adapters(self, client, mock_service):
        mock_service.get_available_local_adapters.return_value = _available(
            adapters=[_adapter(1, True)]
        )
        response = client.get("/models/llama-3/adapters/local")
        assert response.status_code == 200
        assert len(response.json()["adapters"]) == 1
        assert response.json()["adapters"][0]["available_local"] is True

    def test_returns_200_with_no_local_adapters(self, client, mock_service):
        mock_service.get_available_local_adapters.return_value = _available()
        response = client.get("/models/llama-3/adapters/local")
        assert response.status_code == 200

    def test_passes_model_key_to_service(self, client, mock_service):
        mock_service.get_available_local_adapters.return_value = _available()
        client.get("/models/mistral/adapters/local")
        mock_service.get_available_local_adapters.assert_called_once_with(model_key="mistral")


class TestSaveNewAdapter:
    def test_returns_200_on_success(self, client, mock_service):
        mock_service.download_remote_adapter.return_value = _adapter(version=3, available_local=True)
        response = client.post("/models/llama-3/adapters", json={"version": 3})
        assert response.status_code == 200
        assert response.json()["version"] == 3
        assert response.json()["available_local"] is True

    def test_missing_body_returns_422(self, client):
        assert client.post("/models/llama-3/adapters", json={}).status_code == 422

    def test_passes_model_key_and_version_to_service(self, client, mock_service):
        mock_service.download_remote_adapter.return_value = _adapter(version=5)
        client.post("/models/llama-3/adapters", json={"version": 5})
        mock_service.download_remote_adapter.assert_called_once_with(
            model_key="llama-3", adapter_version=5
        )

    def test_router_init_export(self):
        from router.adapters import router as r
        assert r is not None

    def test_router_version(self):
        import router.adapters as ra
        assert ra.__version__ == "1.0.0"
