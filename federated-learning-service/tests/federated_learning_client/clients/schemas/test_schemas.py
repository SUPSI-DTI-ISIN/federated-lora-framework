import pytest
from src.federated_learning_client.clients.schemas import DocumentDTO, SectionDTO, ModelPathDTO


class TestSectionDTO:
    def test_valid(self):
        dto = SectionDTO(id=1, title="1. Introduction", content="Some content")
        assert dto.id == 1
        assert dto.title == "1. Introduction"
        assert dto.content == "Some content"

    def test_missing_field_raises(self):
        with pytest.raises(Exception):
            SectionDTO(id=1, title="T")


class TestDocumentDTO:
    def test_valid_with_sections(self):
        sections = [SectionDTO(id=1, title="1. Intro", content="Content")]
        dto = DocumentDTO(id=1, number="DOC-001", title="My Project",
                          is_externally_approved=False, sections=sections)
        assert dto.id == 1
        assert dto.number == "DOC-001"
        assert len(dto.sections) == 1

    def test_empty_sections(self):
        dto = DocumentDTO(id=1, number="DOC-001", title="My Project",
                          is_externally_approved=False, sections=[])
        assert dto.sections == []

    def test_is_externally_approved_field(self):
        dto = DocumentDTO(id=1, number="DOC-001", title="My Project",
                          is_externally_approved=True, sections=[])
        assert dto.is_externally_approved is True

    def test_missing_field_raises(self):
        with pytest.raises(Exception):
            DocumentDTO(id=1, title="T", sections=[])


class TestModelPathDTO:
    def test_valid_without_adapter(self):
        dto = ModelPathDTO(model_base_path="/models/llama")
        assert dto.model_base_path == "/models/llama"
        assert dto.adapter_path is None

    def test_valid_with_adapter(self):
        dto = ModelPathDTO(model_base_path="/models/llama", adapter_path="/models/llama/adapters/v1")
        assert dto.adapter_path == "/models/llama/adapters/v1"


class TestClientSchemasInit:
    def test_exports(self):
        from src.federated_learning_client.clients.schemas import __all__
        assert "DocumentDTO" in __all__
        assert "SectionDTO" in __all__
        assert "ModelPathDTO" in __all__

    def test_version(self):
        from src.federated_learning_client.clients.schemas import __version__
        assert __version__ == "1.0.0"
