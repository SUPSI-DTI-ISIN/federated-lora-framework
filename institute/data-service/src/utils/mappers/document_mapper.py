from commons.documents import ParsedDocument, ParsedSection
from models import DocumentModel
from .section_mapper import SectionMapper


class DocumentMapper:
    @staticmethod
    def to_model(document: ParsedDocument) -> DocumentModel:
        return DocumentModel(
            number=document.number,
            title=document.title,
            sections=[SectionMapper.to_model(section=section) for section in document.sections]
        )