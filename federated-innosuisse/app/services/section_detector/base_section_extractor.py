from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.section import Section


class BaseSectionExtractor(ABC):
    @abstractmethod
    def extract_document_sections(self, text: str, project_number: str) -> List[Section]:
        ...