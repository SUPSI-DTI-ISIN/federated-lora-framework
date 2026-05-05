import pytest
from pydantic import BaseModel
from schemas.model.file_dto import FileDTO


class TestFileDTO:
    def test_fields_are_set_correctly(self):
        dto = FileDTO(size=1024, rel_path="weights/model.bin", hash="abc123")
        assert dto.size == 1024
        assert dto.rel_path == "weights/model.bin"
        assert dto.hash == "abc123"

    def test_serialization(self):
        assert FileDTO(size=512, rel_path="a.bin", hash="deadbeef").model_dump() == {
            "size": 512, "rel_path": "a.bin", "hash": "deadbeef"
        }

    def test_deserialization(self):
        assert FileDTO.model_validate({"size": 100, "rel_path": "b.bin", "hash": "ff00"}).size == 100

    def test_is_pydantic_model(self):
        assert issubclass(FileDTO, BaseModel)
