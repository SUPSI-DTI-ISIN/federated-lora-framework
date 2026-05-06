import os
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from clients.schemas import ManifestDTO, FileDTO, ModelAdaptersVersionDTO
from schemas.model import AvailableAdaptersDTO, AdapterDTO
from services.adapter.adapter_registry_service import AdapterRegistryService


@pytest.fixture(autouse=True)
def reset_singleton():
    AdapterRegistryService._AdapterRegistryService__INSTANCE = None
    yield
    AdapterRegistryService._AdapterRegistryService__INSTANCE = None


@pytest.fixture()
def mlflow_client():
    return MagicMock()


@pytest.fixture()
def service(mlflow_client):
    return AdapterRegistryService(mlflow_service_client=mlflow_client)


def _manifest(files=None):
    return ManifestDTO(model_key="llama-3", files=files or [])


def _adapters_dto(versions=None):
    return ModelAdaptersVersionDTO(model_key="llama-3", adapters_version=versions)


class TestGetInstance:
    def test_returns_same_instance(self, mlflow_client):
        i1 = AdapterRegistryService.get_instance(mlflow_service_client=mlflow_client)
        i2 = AdapterRegistryService.get_instance(mlflow_service_client=mlflow_client)
        assert i1 is i2

    def test_creates_new_instance_after_reset(self, mlflow_client):
        i1 = AdapterRegistryService.get_instance(mlflow_service_client=mlflow_client)
        AdapterRegistryService._AdapterRegistryService__INSTANCE = None
        i2 = AdapterRegistryService.get_instance(mlflow_service_client=mlflow_client)
        assert i1 is not i2


class TestGetAvailableAdapters:
    def test_returns_all_not_local_when_adapters_path_missing(self, service, mlflow_client):
        mlflow_client.get_adapters_version.return_value = _adapters_dto(versions=[1, 2])

        with patch("services.adapter.adapter_registry_service.os.path.exists", return_value=False):
            result = service.get_available_adapters(model_key="llama-3")

        assert isinstance(result, AvailableAdaptersDTO)
        assert all(not a.available_local for a in result.adapters)
        assert {a.version for a in result.adapters} == {1, 2}

    def test_returns_none_adapters_when_remote_has_none_and_path_missing(self, service, mlflow_client):
        mlflow_client.get_adapters_version.return_value = _adapters_dto(versions=None)

        with patch("services.adapter.adapter_registry_service.os.path.exists", return_value=False):
            result = service.get_available_adapters(model_key="llama-3")

        assert result.adapters is None

    def test_returns_all_not_local_when_local_dir_empty(self, service, mlflow_client, tmp_path):
        mlflow_client.get_adapters_version.return_value = _adapters_dto(versions=[1, 2])
        adapters_path = tmp_path / "adapters"
        adapters_path.mkdir()

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(adapters_path)), \
             patch("services.adapter.adapter_registry_service.os.path.exists", return_value=True):
            result = service.get_available_adapters(model_key="llama-3")

        assert all(not a.available_local for a in result.adapters)

    def test_marks_local_adapters_correctly(self, service, mlflow_client, tmp_path):
        mlflow_client.get_adapters_version.return_value = _adapters_dto(versions=[1, 2, 3])
        adapters_path = tmp_path / "adapters"
        # Create local adapter dirs for v1 and v2 (with content)
        for v in [1, 2]:
            vdir = adapters_path / str(v)
            vdir.mkdir(parents=True)
            (vdir / "adapter.bin").write_bytes(b"data")

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(adapters_path)), \
             patch("services.adapter.adapter_registry_service.os.path.exists", return_value=True):
            result = service.get_available_adapters(model_key="llama-3")

        by_version = {a.version: a for a in result.adapters}
        assert by_version[1].available_local is True
        assert by_version[2].available_local is True
        assert by_version[3].available_local is False

    def test_deletes_local_only_adapters_not_in_remote(self, service, mlflow_client, tmp_path):
        # Remote has v1, v2. Local has v1, v2, v99 (orphan).
        mlflow_client.get_adapters_version.return_value = _adapters_dto(versions=[1, 2])
        adapters_path = tmp_path / "adapters"
        for v in [1, 2, 99]:
            vdir = adapters_path / str(v)
            vdir.mkdir(parents=True)
            (vdir / "adapter.bin").write_bytes(b"data")

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(adapters_path)), \
             patch("services.adapter.adapter_registry_service.os.path.exists", return_value=True), \
             patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   side_effect=lambda model_key, version: str(adapters_path / str(version))):
            result = service.get_available_adapters(model_key="llama-3")

        # v99 dir should have been deleted
        assert not (adapters_path / "99").exists()

    def test_returns_empty_adapters_when_remote_versions_none_and_local_exist(self, service, mlflow_client, tmp_path):
        mlflow_client.get_adapters_version.return_value = _adapters_dto(versions=None)
        adapters_path = tmp_path / "adapters"
        vdir = adapters_path / "1"
        vdir.mkdir(parents=True)
        (vdir / "adapter.bin").write_bytes(b"data")

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(adapters_path)), \
             patch("services.adapter.adapter_registry_service.os.path.exists", return_value=True), \
             patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   side_effect=lambda model_key, version: str(adapters_path / str(version))):
            result = service.get_available_adapters(model_key="llama-3")

        assert result.adapters is None


class TestGetAvailableLocalAdapters:
    def test_returns_empty_when_adapters_path_missing(self, service):
        with patch("services.adapter.adapter_registry_service.os.path.exists", return_value=False):
            result = service.get_available_local_adapters(model_key="llama-3")

        assert isinstance(result, AvailableAdaptersDTO)
        assert result.adapters is None

    def test_returns_empty_when_no_local_adapter_dirs(self, service, tmp_path):
        adapters_path = tmp_path / "adapters"
        adapters_path.mkdir()

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(adapters_path)), \
             patch("services.adapter.adapter_registry_service.os.path.exists", return_value=True):
            result = service.get_available_local_adapters(model_key="llama-3")

        assert result.adapters is None

    def test_returns_local_adapters_with_available_local_true(self, service, tmp_path):
        adapters_path = tmp_path / "adapters"
        for v in [1, 3]:
            vdir = adapters_path / str(v)
            vdir.mkdir(parents=True)
            (vdir / "adapter.bin").write_bytes(b"data")

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(adapters_path)), \
             patch("services.adapter.adapter_registry_service.os.path.exists", return_value=True):
            result = service.get_available_local_adapters(model_key="llama-3")

        assert len(result.adapters) == 2
        assert all(a.available_local for a in result.adapters)
        assert {a.version for a in result.adapters} == {1, 3}

    def test_ignores_empty_adapter_dirs(self, service, tmp_path):
        adapters_path = tmp_path / "adapters"
        # v1 has content, v2 is empty
        (adapters_path / "1").mkdir(parents=True)
        (adapters_path / "1" / "adapter.bin").write_bytes(b"data")
        (adapters_path / "2").mkdir(parents=True)  # empty

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(adapters_path)), \
             patch("services.adapter.adapter_registry_service.os.path.exists", return_value=True):
            result = service.get_available_local_adapters(model_key="llama-3")

        assert len(result.adapters) == 1
        assert result.adapters[0].version == 1

    def test_ignores_non_digit_entries(self, service, tmp_path):
        adapters_path = tmp_path / "adapters"
        (adapters_path / "1").mkdir(parents=True)
        (adapters_path / "1" / "adapter.bin").write_bytes(b"data")
        (adapters_path / "not_a_version").mkdir(parents=True)
        (adapters_path / "not_a_version" / "file.bin").write_bytes(b"data")

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(adapters_path)), \
             patch("services.adapter.adapter_registry_service.os.path.exists", return_value=True):
            result = service.get_available_local_adapters(model_key="llama-3")

        assert len(result.adapters) == 1
        assert result.adapters[0].version == 1


class TestDownloadRemoteAdapter:
    def test_returns_adapter_dto_when_all_files_valid(self, service, mlflow_client, tmp_path):
        manifest = _manifest()
        mlflow_client.get_adapter_manifest.return_value = manifest

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(tmp_path)), \
             patch("services.adapter.adapter_registry_service.FileUtils.check_local_files_validity",
                   return_value=[]):
            result = service.download_remote_adapter(model_key="llama-3", adapter_version=1)

        assert isinstance(result, AdapterDTO)
        assert result.version == 1
        assert result.available_local is True

    def test_fetches_missing_files(self, service, mlflow_client, tmp_path):
        manifest = _manifest(files=[FileDTO(size=100, rel_path="adapter.bin", hash="abc")])
        mlflow_client.get_adapter_manifest.return_value = manifest

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(tmp_path)), \
             patch("services.adapter.adapter_registry_service.FileUtils.check_local_files_validity",
                   return_value=["adapter.bin"]), \
             patch("services.adapter.adapter_registry_service.FileUtils.delete_files") as mock_delete, \
             patch("services.adapter.adapter_registry_service.AdapterValidityService.fetch_adapter") as mock_fetch:
            result = service.download_remote_adapter(model_key="llama-3", adapter_version=1)

        mock_delete.assert_called_once()
        mock_fetch.assert_called_once()
        assert result.available_local is True

    def test_does_not_fetch_when_all_files_valid(self, service, mlflow_client, tmp_path):
        manifest = _manifest()
        mlflow_client.get_adapter_manifest.return_value = manifest

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(tmp_path)), \
             patch("services.adapter.adapter_registry_service.FileUtils.check_local_files_validity",
                   return_value=[]), \
             patch("services.adapter.adapter_registry_service.AdapterValidityService.fetch_adapter") as mock_fetch:
            service.download_remote_adapter(model_key="llama-3", adapter_version=1)

        mock_fetch.assert_not_called()


class TestDeleteAdapterVersion:
    def test_deletes_existing_adapter_dir(self, service, tmp_path):
        adapter_dir = tmp_path / "1"
        adapter_dir.mkdir()
        (adapter_dir / "adapter.bin").write_bytes(b"data")

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(adapter_dir)):
            AdapterRegistryService._AdapterRegistryService__delete_adapter_version(
                model_key="llama-3", adapter_version=1
            )

        assert not adapter_dir.exists()

    def test_raises_file_not_found_when_path_missing(self, service, tmp_path):
        missing_path = tmp_path / "nonexistent"

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(missing_path)):
            with pytest.raises(FileNotFoundError):
                AdapterRegistryService._AdapterRegistryService__delete_adapter_version(
                    model_key="llama-3", adapter_version=99
                )


class TestAdapterServiceInit:
    def test_exports(self):
        import services.adapter as sa
        assert "AdapterRegistryServiceInterface" in sa.__all__
        assert "get_adapter_registry_service" in sa.__all__

    def test_version(self):
        import services.adapter as sa
        assert sa.__version__ == "1.0.0"
