import pytest
from pydantic import BaseModel
from schemas.model.model_adapters_version_dto import ModelAdaptersVersionDTO


class TestModelAdaptersVersionDTO:
    def test_adapters_version_defaults_to_none(self):
        dto = ModelAdaptersVersionDTO(model_key="llama-2")
        assert dto.model_key == "llama-2"
        assert dto.adapters_version is None

    def test_accepts_version_list(self):
        assert ModelAdaptersVersionDTO(model_key="m", adapters_version=[1, 2, 3]).adapters_version == [1, 2, 3]

    def test_accepts_empty_version_list(self):
        assert ModelAdaptersVersionDTO(model_key="m", adapters_version=[]).adapters_version == []

    def test_serialization(self):
        data = ModelAdaptersVersionDTO(model_key="m", adapters_version=[1]).model_dump()
        assert data == {"model_key": "m", "adapters_version": [1]}

    def test_is_pydantic_model(self):
        assert issubclass(ModelAdaptersVersionDTO, BaseModel)
