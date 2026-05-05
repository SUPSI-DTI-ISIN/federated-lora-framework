import pytest
from pathlib import Path
from unittest.mock import patch

from schemas.model import ManifestDTO


@pytest.fixture(autouse=True)
def reset_singleton():
    from services.model.model_registry_service import ModelRegistryService
    ModelRegistryService._ModelRegistryService__INSTANCE = None
    yield
    ModelRegistryService._ModelRegistryService__INSTANCE = None


@pytest.fixture()
def service():
    from services.model.model_registry_service import ModelRegistryService
    return ModelRegistryService.get_instance()


class TestGetInstance:
    def test_returns_same_object_on_repeated_calls(self):
        from services.model.model_registry_service import ModelRegistryService
        assert ModelRegistryService.get_instance() is ModelRegistryService.get_instance()

    def test_returns_non_none_instance(self):
        from services.model.model_registry_service import ModelRegistryService
        assert ModelRegistryService.get_instance() is not None


class TestGetModelManifest:
    def test_raises_when_model_path_does_not_exist(self, service):
        with patch("services.model.model_registry_service.ModelPathUtils.get_model_base_path",
                   return_value="/nonexistent/path"), \
             patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(FileNotFoundError) as exc_info:
                service.get_model_manifest(model_key="missing-model")

        assert "missing-model" in str(exc_info.value)

    def test_returns_manifest_when_path_exists(self, service, tmp_path):
        model_dir = tmp_path / "base"
        model_dir.mkdir()
        (model_dir / "weights.bin").write_bytes(b"data")

        with patch("services.model.model_registry_service.ModelPathUtils.get_model_base_path",
                   return_value=str(model_dir)):
            result = service.get_model_manifest(model_key="my-model")

        assert isinstance(result, ManifestDTO)
        assert result.model_key == "my-model"
        assert len(result.files) == 1

    def test_returns_empty_files_list_for_empty_directory(self, service, tmp_path):
        model_dir = tmp_path / "base"
        model_dir.mkdir()

        with patch("services.model.model_registry_service.ModelPathUtils.get_model_base_path",
                   return_value=str(model_dir)):
            assert service.get_model_manifest(model_key="empty-model").files == []


class TestGetModelFile:
    def test_raises_when_model_path_does_not_exist(self, service):
        with patch("services.model.model_registry_service.ModelPathUtils.get_model_base_path",
                   return_value="/nonexistent"), \
             patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(FileNotFoundError) as exc_info:
                service.get_model_file(model_key="missing", file_name="weights.bin")

        assert "missing" in str(exc_info.value)

    def test_returns_path_when_file_exists(self, service, tmp_path):
        model_dir = tmp_path / "base"
        model_dir.mkdir()
        f = model_dir / "weights.bin"
        f.write_bytes(b"w")

        with patch("services.model.model_registry_service.ModelPathUtils.get_model_base_path",
                   return_value=str(model_dir)):
            assert service.get_model_file(model_key="m", file_name="weights.bin") == f

    def test_raises_when_file_missing_in_existing_directory(self, service, tmp_path):
        model_dir = tmp_path / "base"
        model_dir.mkdir()

        with patch("services.model.model_registry_service.ModelPathUtils.get_model_base_path",
                   return_value=str(model_dir)):
            with pytest.raises(FileNotFoundError):
                service.get_model_file(model_key="m", file_name="missing.bin")
