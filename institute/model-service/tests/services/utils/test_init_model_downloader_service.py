import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from clients.schemas import ManifestDTO, FileDTO
from services.utils.init_model_downloader_service import InitModelDownloaderService


@pytest.fixture(autouse=True)
def reset_singleton():
    InitModelDownloaderService._INSTANCE = None
    yield
    InitModelDownloaderService._INSTANCE = None


@pytest.fixture()
def mlflow_client():
    return MagicMock()


@pytest.fixture()
def service(mlflow_client):
    return InitModelDownloaderService(mlflow_service_client=mlflow_client)


def _manifest(files=None):
    return ManifestDTO(model_key="llama-3", files=files or [])


class TestGetInstance:
    def test_returns_same_instance(self, mlflow_client):
        i1 = InitModelDownloaderService.get_instance(mlflow_service_client=mlflow_client)
        i2 = InitModelDownloaderService.get_instance(mlflow_service_client=mlflow_client)
        assert i1 is i2

    def test_creates_new_instance_after_reset(self, mlflow_client):
        i1 = InitModelDownloaderService.get_instance(mlflow_service_client=mlflow_client)
        InitModelDownloaderService._INSTANCE = None
        i2 = InitModelDownloaderService.get_instance(mlflow_service_client=mlflow_client)
        assert i1 is not i2


class TestDownloadBaseModel:
    def test_does_not_fetch_when_all_files_valid(self, service, mlflow_client, tmp_path):
        manifest = _manifest()
        mlflow_client.get_model_base_manifest.return_value = manifest

        with patch("services.utils.init_model_downloader_service.ModelPathUtils.get_model_base_path",
                   return_value=str(tmp_path)), \
             patch("services.utils.init_model_downloader_service.FileUtils.check_local_files_validity",
                   return_value=[]), \
             patch("services.utils.init_model_downloader_service.ModelValidityService.fetch_model") as mock_fetch:
            service.download_base_model(model_key="llama-3")

        mock_fetch.assert_not_called()

    def test_fetches_missing_files(self, service, mlflow_client, tmp_path):
        manifest = _manifest(files=[FileDTO(size=100, rel_path="model.bin", hash="abc")])
        mlflow_client.get_model_base_manifest.return_value = manifest

        with patch("services.utils.init_model_downloader_service.ModelPathUtils.get_model_base_path",
                   return_value=str(tmp_path)), \
             patch("services.utils.init_model_downloader_service.FileUtils.check_local_files_validity",
                   return_value=["model.bin"]), \
             patch("services.utils.init_model_downloader_service.FileUtils.delete_files") as mock_delete, \
             patch("services.utils.init_model_downloader_service.ModelValidityService.fetch_model") as mock_fetch:
            service.download_base_model(model_key="llama-3")

        mock_delete.assert_called_once()
        mock_fetch.assert_called_once()

    def test_calls_get_model_base_manifest(self, service, mlflow_client, tmp_path):
        manifest = _manifest()
        mlflow_client.get_model_base_manifest.return_value = manifest

        with patch("services.utils.init_model_downloader_service.ModelPathUtils.get_model_base_path",
                   return_value=str(tmp_path)), \
             patch("services.utils.init_model_downloader_service.FileUtils.check_local_files_validity",
                   return_value=[]):
            service.download_base_model(model_key="llama-3")

        mlflow_client.get_model_base_manifest.assert_called_once_with(model_key="llama-3")


class TestUtilsServiceInit:
    def test_exports(self):
        import services.utils as su
        assert "InitModelDownloaderServiceInterface" in su.__all__
        assert "build_init_model_downloader_service" in su.__all__

    def test_version(self):
        import services.utils as su
        assert su.__version__ == "1.0.0"
