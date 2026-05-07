import pytest
from commons.file_utils import FileUtils


class TestFileUtils:
    def test_returns_path_when_file_exists(self, tmp_path):
        f = tmp_path / "model.bin"
        f.write_bytes(b"data")

        assert FileUtils.join_paths(base_path=tmp_path, file_name="model.bin") == f

    def test_raises_when_file_does_not_exist(self, tmp_path):
        with pytest.raises(FileNotFoundError) as exc_info:
            FileUtils.join_paths(base_path=tmp_path, file_name="missing.bin")

        assert "missing.bin" in str(exc_info.value)
        assert "not existing" in str(exc_info.value)

    def test_works_with_nested_file_path(self, tmp_path):
        sub = tmp_path / "sub"
        sub.mkdir()
        f = sub / "nested.txt"
        f.write_text("hi")

        assert FileUtils.join_paths(base_path=tmp_path, file_name="sub/nested.txt") == f
