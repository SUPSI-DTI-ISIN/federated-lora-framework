import hashlib
from pathlib import Path
from commons.file_hash_utils import FileHashUtils


class TestFileHashUtils:
    def test_returns_sha256_hex_digest(self, tmp_path):
        test_file = tmp_path / "test.bin"
        content = b"hello world"
        test_file.write_bytes(content)

        expected = hashlib.sha256(content).hexdigest()
        result = FileHashUtils.get_file_hash(file_path=test_file)

        assert result == expected

    def test_different_content_gives_different_hash(self, tmp_path):
        f1 = tmp_path / "a.bin"
        f2 = tmp_path / "b.bin"
        f1.write_bytes(b"content A")
        f2.write_bytes(b"content B")

        assert FileHashUtils.get_file_hash(f1) != FileHashUtils.get_file_hash(f2)

    def test_same_content_gives_same_hash(self, tmp_path):
        f1 = tmp_path / "a.bin"
        f2 = tmp_path / "b.bin"
        f1.write_bytes(b"same content")
        f2.write_bytes(b"same content")

        assert FileHashUtils.get_file_hash(f1) == FileHashUtils.get_file_hash(f2)

    def test_handles_large_file_in_chunks(self, tmp_path):
        large_file = tmp_path / "large.bin"
        content = b"x" * (8192 * 3 + 100)  # spans multiple 8192-byte chunks
        large_file.write_bytes(content)

        expected = hashlib.sha256(content).hexdigest()
        assert FileHashUtils.get_file_hash(large_file) == expected
