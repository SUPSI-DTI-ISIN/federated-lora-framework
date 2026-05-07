import builtins
import json
import pytest
from unittest.mock import patch, MagicMock, mock_open


@pytest.fixture()
def fake_app():
    schema = {"openapi": "3.0.0", "info": {"title": "Inference Service", "version": "0.0.0"}}
    app = MagicMock()
    app.openapi.return_value = schema
    return app


@pytest.fixture()
def patch_toml_and_app(fake_app):
    real_open = builtins.open

    def selective_open(file, mode="r", *args, **kwargs):
        if "pyproject.toml" in str(file):
            return mock_open(read_data=b"")()
        return real_open(file, mode, *args, **kwargs)

    with patch("builtins.open", side_effect=selective_open), \
         patch("tomllib.load", return_value={"project": {"version": "2.0.0"}}), \
         patch("extract_openapi.create_app", return_value=fake_app):
        yield


class TestSaveOpenapi:
    def test_writes_json_file_with_version_from_toml(self, tmp_path, patch_toml_and_app):
        from extract_openapi import save_openapi
        output_file = tmp_path / "openapi.json"
        save_openapi(output_path=str(output_file))
        assert output_file.exists()
        assert json.loads(output_file.read_text())["info"]["version"] == "2.0.0"

    def test_creates_parent_directories(self, tmp_path, patch_toml_and_app):
        from extract_openapi import save_openapi
        nested = tmp_path / "nested" / "dir" / "openapi.json"
        save_openapi(output_path=str(nested))
        assert nested.exists()

    def test_version_in_output_matches_toml(self, tmp_path):
        real_open = builtins.open

        def selective_open(file, mode="r", *args, **kwargs):
            if "pyproject.toml" in str(file):
                return mock_open(read_data=b"")()
            return real_open(file, mode, *args, **kwargs)

        fake_app = MagicMock()
        fake_app.openapi.return_value = {"openapi": "3.0.0", "info": {"title": "T", "version": "old"}}

        with patch("builtins.open", side_effect=selective_open), \
             patch("tomllib.load", return_value={"project": {"version": "9.9.9"}}), \
             patch("extract_openapi.create_app", return_value=fake_app):
            from extract_openapi import save_openapi
            output_file = tmp_path / "out.json"
            save_openapi(output_path=str(output_file))

        assert json.loads(output_file.read_text())["info"]["version"] == "9.9.9"

    def test_default_output_path_is_openapi_json(self, tmp_path, monkeypatch, patch_toml_and_app):
        from extract_openapi import save_openapi
        monkeypatch.chdir(tmp_path)
        save_openapi()
        assert (tmp_path / "openapi.json").exists()
