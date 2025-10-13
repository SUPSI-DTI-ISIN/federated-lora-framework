from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Metadata:
    filename: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
        }