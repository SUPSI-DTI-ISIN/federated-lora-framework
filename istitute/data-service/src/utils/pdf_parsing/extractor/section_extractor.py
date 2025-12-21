import re
from dataclasses import dataclass

from typing import List, Optional
from schemas.documents import SectionDTO

@dataclass
class SectionUtil:
    title: str
    start_pos: Optional[int] = None
    start_content_pos: Optional[int] = None
    content: str = ""

class SectionExtractor:
    _section_re_pattern = re.compile(r"""
                (?m) 
                ^                               
                (?:
                    (?P<num1>\d+)\.[^\S\r\n]+(?P<title1>[^\n]+)    
                    |
                    (?P<num2>\d+(?:\.\d+)+)[^\S\r\n]+(?P<title2>[^\n]+) 
                )
                """,
                re.VERBOSE,
            )

    @classmethod
    def extract_document_sections(cls, text: str, project_number: str) -> List[SectionDTO]:
        sections: List[SectionUtil] = cls._get_raw_sections(text)

        sections = cls._remove_non_valid_sections(raw_sections=sections, project_number=project_number)

        sections_dto: List[SectionDTO] = cls._get_content_for_sections(sections, text)

        return sections_dto


    @classmethod
    def _remove_non_valid_sections(cls, raw_sections: List[SectionUtil], project_number: str) -> List[SectionUtil]:
        items_counter = dict()

        for item in raw_sections:
            items_counter[item.title] = items_counter.get(item.title, 0) + 1

        result: List[SectionUtil] = []

        for item in raw_sections:
            if items_counter.get(item.title, 0) == 1 and project_number not in item.title:
                result.append(item)

        return result

    @staticmethod
    def _get_content_for_sections(sections: List[SectionUtil], text: str) -> List[SectionDTO]:
        result: List[SectionDTO] = []

        for index, section in enumerate(sections):
            start = section.start_content_pos
            end = sections[index + 1].start_pos if index + 1 < len(sections) else len(text)
            content = text[start:end].strip()
            result.append(SectionDTO(
                title=section.title,
                content=content
            ))

        return result

    @classmethod
    def _get_raw_sections(cls, text: str) -> List[SectionUtil]:
        raw_items: List[SectionUtil] = []
        for match in cls._section_re_pattern.finditer(text):
            if match.group("num1"):
                number = match.group("num1") + "."
                title = match.group("title1").strip()
            else:
                number = match.group("num2")
                title = match.group("title2").strip()

            if not title:
                continue

            raw_items.append(SectionUtil(
                title=number + " " + title,
                start_pos=match.start(),
                start_content_pos=match.end()
            ))

        return raw_items