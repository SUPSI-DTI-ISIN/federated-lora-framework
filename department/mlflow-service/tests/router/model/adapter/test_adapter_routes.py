import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from router.model.adapter.routes import router, get_adapter_registry_service, jwt_validator
from schemas.model import ModelAdaptersVersionDTO, ManifestDTO, FileDTO


def _make_client(mock_svc, mock_user=None):
    app = FastAPI()
    app.dependency_overrides[get_adapter_registry_service] = lambda: mock_svc
    if mock_user is not None:
        app.dependency_overrides[jwt_validator.get_current_user_required] = lambda: mock_user
    app.include_router(router)
    return TestClient(app)


class TestGetAdaptersVersion:
    def test_returns_200_with_versions(self, mock_adapter_service):
        mock_adapter_service.get_adapters_version.return_value = ModelAdaptersVersionDTO(
            model_key="m", adapters_version=[1, 2]
        )
        response = _make_client(mock_adapter_service).get("/model/m/adapters")

        assert response.status_code == 200
        data = response.json()
        assert data["model_key"] == "m"
        assert data["adapters_version"] == [1, 2]

    def test_returns_200_with_null_versions_when_none(self, mock_adapter_service):
        mock_adapter_service.get_adapters_version.return_value = ModelAdaptersVersionDTO(model_key="m")
        response = _make_client(mock_adapter_service).get("/model/m/adapters")

        assert response.status_code == 200
        assert response.json()["adapters_version"] is None

    def test_calls_service_with_correct_model_key(self, mock_adapter_service):
        mock_adapter_service.get_adapters_version.return_value = ModelAdaptersVersionDTO(model_key="llama")
        _make_client(mock_adapter_service).get("/model/llama/adapters")

        mock_adapter_service.get_adapters_version.assert_called_once_with(model_key="llama")


class TestGetAdapterManifest:
    def test_returns_200_with_manifest(self, mock_adapter_service):
        mock_adapter_service.get_adapter_manifest.return_value = ManifestDTO(
            model_key="m", files=[FileDTO(size=1, rel_path="w.bin", hash="abc")]
        )
        response = _make_client(mock_adapter_service).get("/model/m/adapters/1/manifest")

        assert response.status_code == 200
        assert response.json()["model_key"] == "m"

    def test_returns_404_when_adapter_not_found(self, mock_adapter_service):
        mock_adapter_service.get_adapter_manifest.side_effect = FileNotFoundError("no adapter")
        response = _make_client(mock_adapter_service).get("/model/m/adapters/99/manifest")

        assert response.status_code == 404
        assert "no adapter" in response.json()["detail"]

    def test_calls_service_with_correct_params(self, mock_adapter_service):
        mock_adapter_service.get_adapter_manifest.return_value = ManifestDTO(model_key="m")
        _make_client(mock_adapter_service).get("/model/m/adapters/3/manifest")

        mock_adapter_service.get_adapter_manifest.assert_called_once_with(model_key="m", adapter_version=3)


class TestGetAdapterFile:
    def test_returns_200_with_file_content(self, mock_adapter_service, tmp_path):
        f = tmp_path / "weights.bin"
        f.write_bytes(b"data")
        mock_adapter_service.get_adapter_file.return_value = f
        response = _make_client(mock_adapter_service).get("/model/m/adapters/1/file_name/weights.bin")

        assert response.status_code == 200
        assert response.content == b"data"

    def test_returns_404_when_file_not_found(self, mock_adapter_service):
        mock_adapter_service.get_adapter_file.side_effect = FileNotFoundError("no file")
        response = _make_client(mock_adapter_service).get("/model/m/adapters/1/file_name/missing.bin")

        assert response.status_code == 404
        assert "no file" in response.json()["detail"]

    def test_calls_service_with_correct_params(self, mock_adapter_service, tmp_path):
        f = tmp_path / "f.bin"
        f.write_bytes(b"x")
        mock_adapter_service.get_adapter_file.return_value = f
        _make_client(mock_adapter_service).get("/model/m/adapters/2/file_name/f.bin")

        mock_adapter_service.get_adapter_file.assert_called_once_with(
            model_key="m", adapter_version=2, file_name="f.bin"
        )


class TestDeleteAdapterVersion:
    def test_returns_204_on_success(self, mock_adapter_service):
        response = _make_client(mock_adapter_service, mock_user=MagicMock()).delete("/model/m/adapters/1")
        assert response.status_code == 204

    def test_calls_service_with_correct_params(self, mock_adapter_service):
        _make_client(mock_adapter_service, mock_user=MagicMock()).delete("/model/m/adapters/5")

        mock_adapter_service.delete_adapter_version.assert_called_once_with(
            model_key="m", adapter_version=5
        )

    def test_delete_route_declares_jwt_dependency(self):
        import inspect
        from router.model.adapter.routes import delete_adapter_version
        sig = inspect.signature(delete_adapter_version)
        param_defaults = [p.default for p in sig.parameters.values()]
        from fastapi import params as fastapi_params
        depends_callables = [
            d.dependency for d in param_defaults
            if isinstance(d, fastapi_params.Depends)
        ]
        assert jwt_validator.get_current_user_required in depends_callables
