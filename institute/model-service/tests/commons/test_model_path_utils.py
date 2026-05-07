import os
from commons.model_path_utils import ModelPathUtils


class TestModelPathUtils:
    def test_get_model_base_path(self):
        result = ModelPathUtils.get_model_base_path(model_key="llama-3")
        assert "llama-3" in result
        assert result.endswith("base")

    def test_get_model_adapters_path(self):
        result = ModelPathUtils.get_model_adapters_path(model_key="llama-3")
        assert "llama-3" in result
        assert result.endswith("adapters")

    def test_get_model_adapter_path_by_version(self):
        result = ModelPathUtils.get_model_adapter_path_by_version(model_key="llama-3", version=2)
        assert "llama-3" in result
        assert "adapters" in result
        assert "2" in result

    def test_paths_use_model_base_path(self):
        base = ModelPathUtils.get_model_base_path(model_key="llama-3")
        adapters = ModelPathUtils.get_model_adapters_path(model_key="llama-3")
        assert ModelPathUtils.MODEL_BASE_PATH in base
        assert ModelPathUtils.MODEL_BASE_PATH in adapters

    def test_adapter_path_version_is_string(self):
        result = ModelPathUtils.get_model_adapter_path_by_version(model_key="llama-3", version=5)
        assert os.path.join("adapters", "5") in result
