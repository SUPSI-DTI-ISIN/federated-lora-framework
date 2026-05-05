import pytest
from pydantic import BaseModel
from schemas.model.manifest_dto import ManifestDTO
from schemas.model.file_dto import FileDTO


class TestManifestDTO:
    def test_defaults_to_empty_files_list(self):
        dto = ManifestDTO(model_key="llama-2")
        assert dto.model_key == "llama-2"
        assert dto.files == []

    def test_accepts_file_list(self):
        files = [FileDTO(size=10, rel_path="a.bin", hash="h1")]
        dto = ManifestDTO(model_key="llama-2", files=files)
        assert len(dto.files) == 1
        assert dto.files[0].rel_path == "a.bin"

    def test_serialization(self):
        data = ManifestDTO(model_key="m").model_dump()
        assert data["model_key"] == "m"
        assert data["files"] == []

    def test_is_pydantic_model(self):
        assert issubclass(ManifestDTO, BaseModel)

    def test_multiple_files(self):
        files = [
            FileDTO(size=1, rel_path="a.bin", hash="h1"),
            FileDTO(size=2, rel_path="b.bin", hash="h2"),
        ]
        assert len(ManifestDTO(model_key="m", files=files).files) == 2
