from dataclasses import dataclass
from typing import Any, Dict, List
from app.model.section import Section

@dataclass
class DocumentStructure:
    filename: str
    metadata: Dict[str, Any]
    sections: List[Section]

    def to_json(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
            "metadata": self.metadata,
            "sections": [section.to_dict() for section in self.sections]
        }