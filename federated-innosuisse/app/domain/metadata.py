from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Metadata:
    filename: str
    title: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
            "title": self.title,
        }