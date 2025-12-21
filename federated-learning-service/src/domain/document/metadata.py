from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Metadata:
    project_id: str
    filename: str
    title: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "filename": self.filename,
            "title": self.title,
        }