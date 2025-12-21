from models import DocumentModel
from schemas.documents import DocumentDTO
from .section_mapper import SectionMapper


class DocumentMapper:
    @staticmethod
    def to_model(dto: DocumentDTO) -> DocumentModel:
        return DocumentModel(
            id=dto.id,
            title=dto.title,
            sections=[SectionMapper.to_model(dto=sectionDTO) for sectionDTO in dto.sections]
        )