from dataclasses import dataclass
from typing import Any, Dict, List

from app.domain.metadata import Metadata
from app.domain.section import Section


@dataclass
class Document:
    metadata: Metadata
    sections: List[Section]

    def to_json(self) -> Dict[str, Any]:
        return {
            "metadata": self.metadata.to_dict(),
            "sections": [section.to_dict() for section in self.sections]
        }