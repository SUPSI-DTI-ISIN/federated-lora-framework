from commons.documents import ParsedDocument, ParsedSection
from models import DocumentModel, SectionModel
from utils.mappers import DocumentMapper, SectionMapper


class TestSectionMapper:
    def test_to_model_creates_section_model(self):
        section = ParsedSection(title="1. Introduction", content="Some content")
        model = SectionMapper.to_model(section=section)

        assert isinstance(model, SectionModel)
        assert model.title == "1. Introduction"
        assert model.content == "Some content"


class TestDocumentMapper:
    def test_to_model_creates_document_model(self):
        sections = [
            ParsedSection(title="1. Intro", content="Content 1"),
            ParsedSection(title="2. Methods", content="Content 2"),
        ]
        doc = ParsedDocument(number="DOC-001", title="My Project", sections=sections)
        model = DocumentMapper.to_model(document=doc)

        assert isinstance(model, DocumentModel)
        assert model.number == "DOC-001"
        assert model.title == "My Project"
        assert len(model.sections) == 2

    def test_to_model_with_empty_sections(self):
        doc = ParsedDocument(number="DOC-002", title="Empty Doc", sections=[])
        model = DocumentMapper.to_model(document=doc)

        assert model.number == "DOC-002"
        assert model.sections == []

    def test_sections_are_section_models(self):
        sections = [ParsedSection(title="1. Intro", content="Content")]
        doc = ParsedDocument(number="DOC-001", title="Doc", sections=sections)
        model = DocumentMapper.to_model(document=doc)

        assert all(isinstance(s, SectionModel) for s in model.sections)


class TestMappersInit:
    def test_exports_document_mapper(self):
        from utils.mappers import DocumentMapper as DM
        assert DM is DocumentMapper

    def test_exports_section_mapper(self):
        from utils.mappers import SectionMapper as SM
        assert SM is SectionMapper

    def test_version(self):
        import utils.mappers as um
        assert um.__version__ == "1.0.0"
