import pytest
from clients.schemas import ModelPathDTO


class TestModelPathDTO:
    def test_valid_with_adapter(self):
        dto = ModelPathDTO(model_base_path="/models/llama", adapter_path="/models/llama/adapters/v1")
        assert dto.model_base_path == "/models/llama"
        assert dto.adapter_path == "/models/llama/adapters/v1"

    def test_adapter_path_can_be_none(self):
        dto = ModelPathDTO(model_base_path="/models/llama", adapter_path=None)
        assert dto.adapter_path is None

    def test_missing_base_path_raises(self):
        with pytest.raises(Exception):
            ModelPathDTO(adapter_path=None)


class TestClientSchemasInit:
    def test_exports_model_path_dto(self):
        from clients.schemas import ModelPathDTO as D
        assert D is ModelPathDTO

    def test_version(self):
        import clients.schemas as cs
        assert cs.__version__ == "1.0.0"
