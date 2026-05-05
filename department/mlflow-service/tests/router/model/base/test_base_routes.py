import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from router.model.base.routes import router, get_model_registry_service
from schemas.model import ManifestDTO, FileDTO


def _make_client(mock_svc):
    app = FastAPI()
    app.dependency_overrides[get_model_registry_service] = lambda: mock_svc
    app.include_router(router)
    return TestClient(app)


class TestGetModelBaseManifest:
    def test_returns_200_with_manifest(self, mock_model_service):
        mock_model_service.get_model_manifest.return_value = ManifestDTO(
            model_key="llama", files=[FileDTO(size=10, rel_path="w.bin", hash="h")]
        )
        response = _make_client(mock_model_service).get("/model/llama/manifest")

        assert response.status_code == 200
        data = response.json()
        assert data["model_key"] == "llama"
        assert len(data["files"]) == 1

    def test_returns_404_when_model_not_found(self, mock_model_service):
        mock_model_service.get_model_manifest.side_effect = FileNotFoundError("no model")
        response = _make_client(mock_model_service).get("/model/missing/manifest")

        assert response.status_code == 404
        assert "no model" in response.json()["detail"]

    def test_calls_service_with_correct_model_key(self, mock_model_service):
        mock_model_service.get_model_manifest.return_value = ManifestDTO(model_key="m")
        _make_client(mock_model_service).get("/model/my-model/manifest")

        mock_model_service.get_model_manifest.assert_called_once_with(model_key="my-model")

    def test_returns_empty_files_list(self, mock_model_service):
        mock_model_service.get_model_manifest.return_value = ManifestDTO(model_key="m")
        response = _make_client(mock_model_service).get("/model/m/manifest")

        assert response.status_code == 200
        assert response.json()["files"] == []


class TestGetModelBaseFile:
    def test_returns_200_with_file_content(self, mock_model_service, tmp_path):
        f = tmp_path / "weights.bin"
        f.write_bytes(b"model-data")
        mock_model_service.get_model_file.return_value = f
        response = _make_client(mock_model_service).get("/model/m/file_name/weights.bin")

        assert response.status_code == 200
        assert response.content == b"model-data"

    def test_returns_404_when_model_not_found(self, mock_model_service):
        mock_model_service.get_model_file.side_effect = FileNotFoundError("no model")
        response = _make_client(mock_model_service).get("/model/missing/file_name/w.bin")

        assert response.status_code == 404
        assert "no model" in response.json()["detail"]

    def test_returns_404_when_file_not_found(self, mock_model_service):
        mock_model_service.get_model_file.side_effect = FileNotFoundError("no file")
        response = _make_client(mock_model_service).get("/model/m/file_name/missing.bin")

        assert response.status_code == 404

    def test_calls_service_with_correct_params(self, mock_model_service, tmp_path):
        f = tmp_path / "f.bin"
        f.write_bytes(b"x")
        mock_model_service.get_model_file.return_value = f
        _make_client(mock_model_service).get("/model/llama/file_name/config.json")

        mock_model_service.get_model_file.assert_called_once_with(
            model_key="llama", file_name="config.json"
        )

    def test_response_content_type_is_octet_stream(self, mock_model_service, tmp_path):
        f = tmp_path / "f.bin"
        f.write_bytes(b"bytes")
        mock_model_service.get_model_file.return_value = f
        response = _make_client(mock_model_service).get("/model/m/file_name/f.bin")

        assert "application/octet-stream" in response.headers["content-type"]
