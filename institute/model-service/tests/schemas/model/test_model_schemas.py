import pytest
from schemas.model import AvailableAdaptersDTO, AdapterDTO, NewAdapterRequestDTO, ModelPathDTO


class TestAdapterDTO:
    def test_valid(self):
        dto = AdapterDTO(version=1, available_local=True)
        assert dto.version == 1
        assert dto.available_local is True

    def test_available_local_false(self):
        dto = AdapterDTO(version=2, available_local=False)
        assert dto.available_local is False

    def test_missing_field_raises(self):
        with pytest.raises(Exception):
            AdapterDTO(version=1)


class TestAvailableAdaptersDTO:
    def test_valid_with_adapters(self):
        adapters = [AdapterDTO(version=1, available_local=True)]
        dto = AvailableAdaptersDTO(model_key="llama-3", adapters=adapters)
        assert dto.model_key == "llama-3"
        assert len(dto.adapters) == 1

    def test_adapters_defaults_to_none(self):
        dto = AvailableAdaptersDTO(model_key="llama-3")
        assert dto.adapters is None

    def test_missing_model_key_raises(self):
        with pytest.raises(Exception):
            AvailableAdaptersDTO()


class TestNewAdapterRequestDTO:
    def test_valid(self):
        dto = NewAdapterRequestDTO(version=3)
        assert dto.version == 3

    def test_missing_version_raises(self):
        with pytest.raises(Exception):
            NewAdapterRequestDTO()


class TestModelPathDTO:
    def test_valid_without_adapter(self):
        dto = ModelPathDTO(model_base_path="/models/llama")
        assert dto.model_base_path == "/models/llama"
        assert dto.adapter_path is None

    def test_valid_with_adapter(self):
        dto = ModelPathDTO(model_base_path="/models/llama", adapter_path="/models/llama/adapters/v1")
        assert dto.adapter_path == "/models/llama/adapters/v1"

    def test_missing_base_path_raises(self):
        with pytest.raises(Exception):
            ModelPathDTO()


class TestSchemasModelInit:
    def test_exports(self):
        import schemas.model as sm
        assert "AvailableAdaptersDTO" in sm.__all__
        assert "AdapterDTO" in sm.__all__
        assert "NewAdapterRequestDTO" in sm.__all__
        assert "ModelPathDTO" in sm.__all__
