from models import SectionModel
from commons.documents import ParsedSection


class SectionMapper:
    @staticmethod
    def to_model(section: ParsedSection) -> SectionModel:
        return SectionModel(
            title=section.title,
            content=section.content
        )