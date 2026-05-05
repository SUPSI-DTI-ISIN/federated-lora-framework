import pytest
from commons.adapter_utils import AdapterUtils


class TestAdapterUtils:
    def test_returns_true_when_all_required_files_exist(self, tmp_path):
        adapter_dir = tmp_path / "adapter"
        adapter_dir.mkdir()
        (adapter_dir / "adapter_config.json").write_text("{}")
        (adapter_dir / "adapter_model.safetensors").write_bytes(b"data")

        assert AdapterUtils.is_valid_adapter(path=adapter_dir) is True

    def test_returns_false_when_path_does_not_exist(self, tmp_path):
        assert AdapterUtils.is_valid_adapter(path=tmp_path / "nonexistent") is False

    def test_returns_false_when_adapter_config_missing(self, tmp_path):
        adapter_dir = tmp_path / "adapter"
        adapter_dir.mkdir()
        (adapter_dir / "adapter_model.safetensors").write_bytes(b"data")

        assert AdapterUtils.is_valid_adapter(path=adapter_dir) is False

    def test_returns_false_when_safetensors_missing(self, tmp_path):
        adapter_dir = tmp_path / "adapter"
        adapter_dir.mkdir()
        (adapter_dir / "adapter_config.json").write_text("{}")

        assert AdapterUtils.is_valid_adapter(path=adapter_dir) is False

    def test_returns_false_when_directory_is_empty(self, tmp_path):
        adapter_dir = tmp_path / "adapter"
        adapter_dir.mkdir()

        assert AdapterUtils.is_valid_adapter(path=adapter_dir) is False
