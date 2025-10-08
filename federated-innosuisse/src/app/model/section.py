from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class Section:
    number: str
    title: str
    level: int
    start_content_pos: Optional[int] = None
    parent_number: Optional[str] = None
    content: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "section_number": self.number,
            "section_title": self.title,
            "section_content": self.content,
            "section_level": self.level,
            "section_parent": self.parent_number
        }