from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class Section:
    title: str
    start_pos: Optional[int] = None
    start_content_pos: Optional[int] = None
    content: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "section_title": self.title,
            "section_content": self.content,
        }