from abc import ABC, abstractmethod
from typing import Any, Dict, List

from app.model.section import Section


class ISectionDetector(ABC):
    @abstractmethod
    def detect_sections(self, text: str) -> List[Section]:
        ...