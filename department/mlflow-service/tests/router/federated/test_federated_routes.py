import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from router.federated.routes import router, get_adapter_registry_service


def _make_client(mock_svc):
    app = FastAPI()
    app.dependency_overrides[get_adapter_registry_service] = lambda: mock_svc
    app.include_router(router)
    return TestClient(app)


class TestFederatedRoutes:
    def test_returns_200_with_new_and_latest_paths(self, mock_adapter_service):
        mock_adapter_service.get_new_adapter_path.return_value = "/tmp/new"
        mock_adapter_service.get_latest_adapter_path.return_value = "/tmp/latest"

        response = _make_client(mock_adapter_service).get("/federated/my-model")

        assert response.status_code == 200
        assert response.json() == {"new_adapter_path": "/tmp/new", "latest_adapter_path": "/tmp/latest"}

    def test_calls_service_with_correct_model_key(self, mock_adapter_service):
        mock_adapter_service.get_new_adapter_path.return_value = "/a"
        mock_adapter_service.get_latest_adapter_path.return_value = "/b"

        _make_client(mock_adapter_service).get("/federated/llama-2")

        mock_adapter_service.get_new_adapter_path.assert_called_once_with(model_key="llama-2")
        mock_adapter_service.get_latest_adapter_path.assert_called_once_with(model_key="llama-2")

    def test_returns_404_when_new_path_raises_file_not_found(self, mock_adapter_service):
        mock_adapter_service.get_new_adapter_path.side_effect = FileNotFoundError("not found")

        response = _make_client(mock_adapter_service).get("/federated/missing-model")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_returns_404_when_latest_path_raises_file_not_found(self, mock_adapter_service):
        mock_adapter_service.get_new_adapter_path.return_value = "/a"
        mock_adapter_service.get_latest_adapter_path.side_effect = FileNotFoundError("no latest")

        response = _make_client(mock_adapter_service).get("/federated/missing-model")

        assert response.status_code == 404

    def test_router_init_export(self):
        from router.federated import router as r
        assert r is not None

    def test_router_version(self):
        import router.federated as rf
        assert rf.__version__ == "1.0.0"
