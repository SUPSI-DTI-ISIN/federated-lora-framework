from models import SectionModel
from schemas.documents import SectionDTO


class SectionMapper:
    @staticmethod
    def to_model(dto: SectionDTO) -> SectionModel:
        return SectionModel(
            title=dto.title,
            content=dto.content
        )