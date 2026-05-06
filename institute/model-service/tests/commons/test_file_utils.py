import hashlib
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from clients.schemas import ManifestDTO, FileDTO
from commons.file_utils import FileUtils


def _make_manifest(model_key="llama-3", files=None):
    return ManifestDTO(model_key=model_key, files=files or [])


def _file_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


class TestCheckLocalFilesValidity:
    def test_returns_empty_list_when_all_files_valid(self, tmp_path):
        content = b"model weights"
        (tmp_path / "model.bin").write_bytes(content)
        manifest = _make_manifest(files=[
            FileDTO(size=len(content), rel_path="model.bin", hash=_file_hash(content))
        ])

        result = FileUtils.check_local_files_validity(target_folder_path=tmp_path, manifest=manifest)
        assert result == []

    def test_returns_missing_file(self, tmp_path):
        manifest = _make_manifest(files=[
            FileDTO(size=100, rel_path="missing.bin", hash="abc123")
        ])

        result = FileUtils.check_local_files_validity(target_folder_path=tmp_path, manifest=manifest)
        assert "missing.bin" in result

    def test_returns_corrupted_file(self, tmp_path):
        (tmp_path / "model.bin").write_bytes(b"corrupted content")
        manifest = _make_manifest(files=[
            FileDTO(size=100, rel_path="model.bin", hash="correct_hash_that_wont_match")
        ])

        result = FileUtils.check_local_files_validity(target_folder_path=tmp_path, manifest=manifest)
        assert "model.bin" in result

    def test_returns_empty_list_for_empty_manifest(self, tmp_path):
        manifest = _make_manifest(files=[])
        result = FileUtils.check_local_files_validity(target_folder_path=tmp_path, manifest=manifest)
        assert result == []

    def test_mixed_valid_and_invalid_files(self, tmp_path):
        valid_content = b"valid"
        (tmp_path / "valid.bin").write_bytes(valid_content)
        manifest = _make_manifest(files=[
            FileDTO(size=len(valid_content), rel_path="valid.bin", hash=_file_hash(valid_content)),
            FileDTO(size=100, rel_path="missing.bin", hash="abc"),
        ])

        result = FileUtils.check_local_files_validity(target_folder_path=tmp_path, manifest=manifest)
        assert "missing.bin" in result
        assert "valid.bin" not in result


class TestDeleteFiles:
    def test_deletes_existing_files(self, tmp_path):
        f = tmp_path / "to_delete.bin"
        f.write_bytes(b"data")
        assert f.exists()

        FileUtils.delete_files(target_folder_path=tmp_path, model_files=["to_delete.bin"])
        assert not f.exists()

    def test_skips_non_existing_files(self, tmp_path):
        FileUtils.delete_files(target_folder_path=tmp_path, model_files=["nonexistent.bin"])

    def test_deletes_multiple_files(self, tmp_path):
        for name in ["a.bin", "b.bin", "c.bin"]:
            (tmp_path / name).write_bytes(b"data")

        FileUtils.delete_files(target_folder_path=tmp_path, model_files=["a.bin", "b.bin"])

        assert not (tmp_path / "a.bin").exists()
        assert not (tmp_path / "b.bin").exists()
        assert (tmp_path / "c.bin").exists()

    def test_empty_list_does_nothing(self, tmp_path):
        f = tmp_path / "keep.bin"
        f.write_bytes(b"data")
        FileUtils.delete_files(target_folder_path=tmp_path, model_files=[])
        assert f.exists()


class TestCommonsInit:
    def test_exports(self):
        import commons
        assert "ModelPathUtils" in commons.__all__
        assert "FileHashUtils" in commons.__all__
        assert "FileUtils" in commons.__all__

    def test_version(self):
        import commons
        assert commons.__version__ == "1.0.0"
