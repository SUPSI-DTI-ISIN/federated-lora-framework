import pytest
from pydantic import BaseModel
from schemas.model.federated_data_dto import FederatedDataDTO


class TestFederatedDataDTO:
    def test_fields_are_set_correctly(self):
        dto = FederatedDataDTO(new_adapter_path="/tmp/new", latest_adapter_path="/tmp/latest")
        assert dto.new_adapter_path == "/tmp/new"
        assert dto.latest_adapter_path == "/tmp/latest"

    def test_serialization(self):
        assert FederatedDataDTO(new_adapter_path="/a", latest_adapter_path="/b").model_dump() == {
            "new_adapter_path": "/a", "latest_adapter_path": "/b"
        }

    def test_is_pydantic_model(self):
        assert issubclass(FederatedDataDTO, BaseModel)

    def test_deserialization(self):
        dto = FederatedDataDTO.model_validate({"new_adapter_path": "/x", "latest_adapter_path": "/y"})
        assert dto.new_adapter_path == "/x"
