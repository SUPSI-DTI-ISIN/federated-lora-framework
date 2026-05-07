from dataclasses import dataclass
from typing import List

from .parsed_section import ParsedSection

@dataclass
class ParsedDocument:
    number: str
    title: str
    sections: List[ParsedSection]