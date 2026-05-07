import pytest
from schemas.documents import (
    DocumentDTO,
    SectionDTO,
    UpdateDocumentTrainableRequestDTO,
    UpdateDocumentExternallyApprovedRequestDTO,
    TrainingSamplesDTO,
    UpdateSectionRequestDTO,
    UploadDocumentRequestDTO,
)


class TestSectionDTO:
    def test_valid_dto(self):
        dto = SectionDTO(id=1, title="1. Intro", content="Some content")
        assert dto.id == 1
        assert dto.title == "1. Intro"
        assert dto.content == "Some content"

    def test_from_attributes(self):
        from models import SectionModel
        section = SectionModel()
        section.id = 5
        section.title = "2. Methods"
        section.content = "Methods content"
        dto = SectionDTO.model_validate(section)
        assert dto.id == 5
        assert dto.title == "2. Methods"

    def test_missing_required_field_raises(self):
        with pytest.raises(Exception):
            SectionDTO(id=1, title="T")


class TestDocumentDTO:
    def test_valid_dto(self):
        sections = [SectionDTO(id=1, title="1. Intro", content="Content")]
        dto = DocumentDTO(id=1, number="DOC-001", title="My Doc", is_trainable=False,
                          is_externally_approved=False, sections=sections)
        assert dto.id == 1
        assert dto.number == "DOC-001"
        assert dto.is_trainable is False
        assert dto.is_externally_approved is False
        assert len(dto.sections) == 1

    def test_from_attributes(self):
        from models import DocumentModel
        doc = DocumentModel()
        doc.id = 3
        doc.number = "DOC-003"
        doc.title = "Test"
        doc.is_trainable = True
        doc.is_externally_approved = True
        doc.sections = []
        dto = DocumentDTO.model_validate(doc)
        assert dto.id == 3
        assert dto.is_trainable is True
        assert dto.is_externally_approved is True

    def test_empty_sections(self):
        dto = DocumentDTO(id=1, number="DOC-001", title="Doc", is_trainable=False,
                          is_externally_approved=False, sections=[])
        assert dto.sections == []

    def test_is_externally_approved_true(self):
        dto = DocumentDTO(id=1, number="DOC-001", title="Doc", is_trainable=False,
                          is_externally_approved=True, sections=[])
        assert dto.is_externally_approved is True


class TestUpdateDocumentTrainableRequestDTO:
    def test_is_trainable_true(self):
        dto = UpdateDocumentTrainableRequestDTO(is_trainable=True)
        assert dto.is_trainable is True

    def test_is_trainable_false(self):
        dto = UpdateDocumentTrainableRequestDTO(is_trainable=False)
        assert dto.is_trainable is False

    def test_missing_field_raises(self):
        with pytest.raises(Exception):
            UpdateDocumentTrainableRequestDTO()


class TestUpdateDocumentExternallyApprovedRequestDTO:
    def test_is_externally_approved_true(self):
        dto = UpdateDocumentExternallyApprovedRequestDTO(is_externally_approved=True)
        assert dto.is_externally_approved is True

    def test_is_externally_approved_false(self):
        dto = UpdateDocumentExternallyApprovedRequestDTO(is_externally_approved=False)
        assert dto.is_externally_approved is False

    def test_missing_field_raises(self):
        with pytest.raises(Exception):
            UpdateDocumentExternallyApprovedRequestDTO()


class TestTrainingSamplesDTO:
    def test_valid_dto(self):
        dto = TrainingSamplesDTO(institute_name="TestInstitute", trainable_samples_number=42)
        assert dto.institute_name == "TestInstitute"
        assert dto.trainable_samples_number == 42


class TestUpdateSectionRequestDTO:
    def test_valid_dto(self):
        dto = UpdateSectionRequestDTO(updated_content="New content")
        assert dto.updated_content == "New content"

    def test_missing_field_raises(self):
        with pytest.raises(Exception):
            UpdateSectionRequestDTO()


class TestSchemasDocumentsInit:
    def test_exports_all(self):
        import schemas.documents as sd
        assert "DocumentDTO" in sd.__all__
        assert "SectionDTO" in sd.__all__
        assert "UpdateDocumentTrainableRequestDTO" in sd.__all__
        assert "UpdateDocumentExternallyApprovedRequestDTO" in sd.__all__
        assert "TrainingSamplesDTO" in sd.__all__
        assert "UpdateSectionRequestDTO" in sd.__all__
        assert "UploadDocumentRequestDTO" in sd.__all__

    def test_version(self):
        import schemas.documents as sd
        assert sd.__version__ == "1.0.0"
