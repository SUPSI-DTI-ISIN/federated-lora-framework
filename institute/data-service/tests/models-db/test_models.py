from models import BaseModel, DocumentModel, SectionModel


class TestDocumentModel:
    def test_tablename(self):
        assert DocumentModel.__tablename__ == "documents"

    def test_can_be_instantiated_with_fields(self):
        doc = DocumentModel()
        doc.id = 1
        doc.number = "DOC-001"
        doc.title = "Test Document"
        doc.is_trainable = False
        doc.is_externally_approved = False

        assert doc.id == 1
        assert doc.number == "DOC-001"
        assert doc.title == "Test Document"
        assert doc.is_trainable is False
        assert doc.is_externally_approved is False

    def test_is_subclass_of_base_model(self):
        assert issubclass(DocumentModel, BaseModel)


class TestSectionModel:
    def test_tablename(self):
        assert SectionModel.__tablename__ == "sections"

    def test_can_be_instantiated_with_fields(self):
        section = SectionModel()
        section.id = 1
        section.document_id = 10
        section.title = "1. Introduction"
        section.content = "This is the introduction."

        assert section.id == 1
        assert section.document_id == 10
        assert section.title == "1. Introduction"
        assert section.content == "This is the introduction."

    def test_is_subclass_of_base_model(self):
        assert issubclass(SectionModel, BaseModel)


class TestModelsInit:
    def test_exports_base_model(self):
        from models import BaseModel as BM
        assert BM is BaseModel

    def test_exports_document_model(self):
        from models import DocumentModel as DM
        assert DM is DocumentModel

    def test_exports_section_model(self):
        from models import SectionModel as SM
        assert SM is SectionModel

    def test_version(self):
        import models
        assert models.__version__ == "1.0.0"

    def test_all_list(self):
        import models
        assert "BaseModel" in models.__all__
        assert "DocumentModel" in models.__all__
        assert "SectionModel" in models.__all__
