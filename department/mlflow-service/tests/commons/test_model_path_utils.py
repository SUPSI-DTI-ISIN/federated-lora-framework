import os
import pytest


class TestModelPathUtils:
    def setup_method(self):
        from commons.model_path_utils import ModelPathUtils
        self._original_base = ModelPathUtils.MODEL_BASE_PATH
        ModelPathUtils.MODEL_BASE_PATH = "/base"

    def teardown_method(self):
        from commons.model_path_utils import ModelPathUtils
        ModelPathUtils.MODEL_BASE_PATH = self._original_base

    def test_get_model_base_path(self):
        from commons.model_path_utils import ModelPathUtils
        assert ModelPathUtils.get_model_base_path("llama-2") == os.path.join("/base", "llama-2", "base")

    def test_get_model_adapters_path(self):
        from commons.model_path_utils import ModelPathUtils
        assert ModelPathUtils.get_model_adapters_path("llama-2") == os.path.join("/base", "llama-2", "adapters")

    def test_get_model_adapter_path_by_version(self):
        from commons.model_path_utils import ModelPathUtils
        assert ModelPathUtils.get_model_adapter_path_by_version("llama-2", version=3) == os.path.join("/base", "llama-2", "adapters", "3")

    def test_get_model_adapter_path_by_version_zero(self):
        from commons.model_path_utils import ModelPathUtils
        assert ModelPathUtils.get_model_adapter_path_by_version("llama-2", version=0) == os.path.join("/base", "llama-2", "adapters", "0")

    def test_get_model_init_adapter_path(self):
        from commons.model_path_utils import ModelPathUtils
        assert ModelPathUtils.get_model_init_adapter_path("llama-2") == os.path.join("/base", "llama-2", "adapters", "init")

    def test_different_model_keys_produce_different_paths(self):
        from commons.model_path_utils import ModelPathUtils
        r1 = ModelPathUtils.get_model_base_path("model-a")
        r2 = ModelPathUtils.get_model_base_path("model-b")
        assert r1 != r2
        assert "model-a" in r1
        assert "model-b" in r2
