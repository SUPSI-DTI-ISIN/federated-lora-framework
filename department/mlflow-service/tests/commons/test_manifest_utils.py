import hashlib
import pytest
from commons.manifest_utils import ManifestUtils
from schemas.model import ManifestDTO


class TestManifestUtils:
    def test_empty_directory_returns_empty_files_list(self, tmp_path):
        result = ManifestUtils.get_manifest(base_path=tmp_path, model_key="my-model")

        assert isinstance(result, ManifestDTO)
        assert result.model_key == "my-model"
        assert result.files == []

    def test_single_file_produces_correct_entry(self, tmp_path):
        content = b"abc"
        (tmp_path / "weights.bin").write_bytes(content)

        result = ManifestUtils.get_manifest(base_path=tmp_path, model_key="m1")

        assert len(result.files) == 1
        assert result.files[0].rel_path == "weights.bin"
        assert result.files[0].size == len(content)
        assert result.files[0].hash == hashlib.sha256(content).hexdigest()

    def test_multiple_files_are_all_included(self, tmp_path):
        (tmp_path / "a.bin").write_bytes(b"aa")
        (tmp_path / "b.bin").write_bytes(b"bbb")

        result = ManifestUtils.get_manifest(base_path=tmp_path, model_key="m2")

        rel_paths = {f.rel_path for f in result.files}
        assert rel_paths == {"a.bin", "b.bin"}

    def test_nested_files_are_included(self, tmp_path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "nested.bin").write_bytes(b"x")
        (tmp_path / "root.bin").write_bytes(b"y")

        result = ManifestUtils.get_manifest(base_path=tmp_path, model_key="m3")

        assert len(result.files) == 2
        rel_paths = {f.rel_path for f in result.files}
        assert "root.bin" in rel_paths
        assert any("nested.bin" in p for p in rel_paths)

    def test_model_key_is_preserved(self, tmp_path):
        result = ManifestUtils.get_manifest(base_path=tmp_path, model_key="special-key")
        assert result.model_key == "special-key"

    def test_subdirectories_without_files_are_not_included(self, tmp_path):
        (tmp_path / "subdir").mkdir()

        result = ManifestUtils.get_manifest(base_path=tmp_path, model_key="k")
        assert result.files == []
