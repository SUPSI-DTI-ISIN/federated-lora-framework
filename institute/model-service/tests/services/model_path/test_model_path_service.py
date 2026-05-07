import pytest
from pathlib import Path
from unittest.mock import patch

from schemas.model import ModelPathDTO
from services.model_path.model_path_service import ModelPathService


@pytest.fixture(autouse=True)
def reset_singleton():
    ModelPathService._ModelPathService__INSTANCE = None
    yield
    ModelPathService._ModelPathService__INSTANCE = None


class TestGetInstance:
    def test_returns_same_instance(self):
        i1 = ModelPathService.get_instance()
        i2 = ModelPathService.get_instance()
        assert i1 is i2

    def test_creates_new_instance_after_reset(self):
        i1 = ModelPathService.get_instance()
        ModelPathService._ModelPathService__INSTANCE = None
        i2 = ModelPathService.get_instance()
        assert i1 is not i2


class TestGetModelPath:
    @pytest.fixture()
    def service(self):
        return ModelPathService()

    def test_returns_model_path_dto_without_adapter(self, service, tmp_path):
        model_base = tmp_path / "llama-3" / "base"
        model_base.mkdir(parents=True)

        with patch("services.model_path.model_path_service.ModelPathUtils.get_model_base_path",
                   return_value=str(model_base)):
            result = service.get_model_path(model_key="llama-3", adapter_version=None)

        assert isinstance(result, ModelPathDTO)
        assert result.adapter_path is None
        assert "llama-3" in result.model_base_path or str(model_base.resolve()) == result.model_base_path

    def test_returns_model_path_dto_with_adapter(self, service, tmp_path):
        model_base = tmp_path / "llama-3" / "base"
        model_base.mkdir(parents=True)
        adapter_path = tmp_path / "llama-3" / "adapters" / "1"
        adapter_path.mkdir(parents=True)

        with patch("services.model_path.model_path_service.ModelPathUtils.get_model_base_path",
                   return_value=str(model_base)), \
             patch("services.model_path.model_path_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(adapter_path)):
            result = service.get_model_path(model_key="llama-3", adapter_version=1)

        assert isinstance(result, ModelPathDTO)
        assert result.adapter_path is not None

    def test_raises_file_not_found_when_base_path_missing(self, service, tmp_path):
        missing_path = str(tmp_path / "nonexistent" / "base")

        with patch("services.model_path.model_path_service.ModelPathUtils.get_model_base_path",
                   return_value=missing_path):
            with pytest.raises(FileNotFoundError, match="llama-3"):
                service.get_model_path(model_key="llama-3", adapter_version=None)

    def test_raises_file_not_found_when_adapter_path_missing(self, service, tmp_path):
        model_base = tmp_path / "llama-3" / "base"
        model_base.mkdir(parents=True)
        missing_adapter = str(tmp_path / "llama-3" / "adapters" / "99")

        with patch("services.model_path.model_path_service.ModelPathUtils.get_model_base_path",
                   return_value=str(model_base)), \
             patch("services.model_path.model_path_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=missing_adapter):
            with pytest.raises(FileNotFoundError, match="99"):
                service.get_model_path(model_key="llama-3", adapter_version=99)

    def test_resolved_paths_are_absolute(self, service, tmp_path):
        model_base = tmp_path / "llama-3" / "base"
        model_base.mkdir(parents=True)

        with patch("services.model_path.model_path_service.ModelPathUtils.get_model_base_path",
                   return_value=str(model_base)):
            result = service.get_model_path(model_key="llama-3", adapter_version=None)

        assert Path(result.model_base_path).is_absolute()


class TestModelPathServiceInit:
    def test_exports(self):
        import services.model_path as smp
        assert "ModelPathServiceInterface" in smp.__all__
        assert "get_model_path_service" in smp.__all__

    def test_version(self):
        import services.model_path as smp
        assert smp.__version__ == "1.0.0"
