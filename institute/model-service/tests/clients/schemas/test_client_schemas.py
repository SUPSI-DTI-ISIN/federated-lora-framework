import pytest
from clients.schemas import FileDTO, ManifestDTO, ModelAdaptersVersionDTO


class TestFileDTO:
    def test_valid(self):
        dto = FileDTO(size=1024, rel_path="config.json", hash="abc123")
        assert dto.size == 1024
        assert dto.rel_path == "config.json"
        assert dto.hash == "abc123"

    def test_missing_field_raises(self):
        with pytest.raises(Exception):
            FileDTO(size=1024, rel_path="config.json")


class TestManifestDTO:
    def test_valid_with_files(self):
        files = [FileDTO(size=100, rel_path="model.bin", hash="abc")]
        dto = ManifestDTO(model_key="llama-3", files=files)
        assert dto.model_key == "llama-3"
        assert len(dto.files) == 1

    def test_files_defaults_to_empty_list(self):
        dto = ManifestDTO(model_key="llama-3")
        assert dto.files == []

    def test_missing_model_key_raises(self):
        with pytest.raises(Exception):
            ManifestDTO()


class TestModelAdaptersVersionDTO:
    def test_valid_with_versions(self):
        dto = ModelAdaptersVersionDTO(model_key="llama-3", adapters_version=[1, 2, 3])
        assert dto.model_key == "llama-3"
        assert dto.adapters_version == [1, 2, 3]

    def test_adapters_version_defaults_to_none(self):
        dto = ModelAdaptersVersionDTO(model_key="llama-3")
        assert dto.adapters_version is None

    def test_missing_model_key_raises(self):
        with pytest.raises(Exception):
            ModelAdaptersVersionDTO()


class TestClientSchemasInit:
    def test_exports(self):
        import clients.schemas as cs
        assert "FileDTO" in cs.__all__
        assert "ManifestDTO" in cs.__all__
        assert "ModelAdaptersVersionDTO" in cs.__all__

    def test_version(self):
        import clients.schemas as cs
        assert cs.__version__ == "1.0.0"
