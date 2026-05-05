import hashlib
import pytest
from commons.file_hash_utils import FileHashUtils


class TestFileHashUtils:
    def test_returns_sha256_hex_digest(self, tmp_path):
        content = b"hello world"
        f = tmp_path / "test.bin"
        f.write_bytes(content)

        assert FileHashUtils.get_file_hash(file_path=f) == hashlib.sha256(content).hexdigest()

    def test_empty_file_returns_empty_sha256(self, tmp_path):
        f = tmp_path / "empty.bin"
        f.write_bytes(b"")

        assert FileHashUtils.get_file_hash(file_path=f) == hashlib.sha256(b"").hexdigest()

    def test_large_file_produces_correct_hash(self, tmp_path):
        content = b"x" * 20_000
        f = tmp_path / "large.bin"
        f.write_bytes(content)

        assert FileHashUtils.get_file_hash(file_path=f) == hashlib.sha256(content).hexdigest()

    def test_different_content_produces_different_hashes(self, tmp_path):
        f1 = tmp_path / "a.bin"
        f2 = tmp_path / "b.bin"
        f1.write_bytes(b"aaa")
        f2.write_bytes(b"bbb")

        assert FileHashUtils.get_file_hash(f1) != FileHashUtils.get_file_hash(f2)

    def test_identical_content_produces_identical_hashes(self, tmp_path):
        f1 = tmp_path / "a.bin"
        f2 = tmp_path / "b.bin"
        f1.write_bytes(b"same")
        f2.write_bytes(b"same")

        assert FileHashUtils.get_file_hash(f1) == FileHashUtils.get_file_hash(f2)
