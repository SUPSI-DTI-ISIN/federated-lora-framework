import re

from typing import List, override

from app.domain.entities.section import Section
from app.services.section_detector.base_section_extractor import BaseSectionExtractor


def _remove_non_valid_sections(raw_sections: List[Section], project_number: str) -> List[Section]:
    items_counter = dict()

    for item in raw_sections:
        items_counter[item.title] = items_counter.get(item.title, 0) + 1

    result: List[Section] = []

    for item in raw_sections:
        if items_counter.get(item.title, 0) == 1 and project_number not in item.title:
            result.append(item)

    return result


def _get_content_for_sections(sections: List[Section], text: str) -> List[Section]:
    result: List[Section] = []

    for index, section in enumerate(sections):
        start = section.start_content_pos
        end = sections[index + 1].start_pos if index + 1 < len(sections) else len(text)
        content = text[start:end].strip()
        section.content = content
        result.append(section)

    return result


class SectionExtractor(BaseSectionExtractor):
    def __init__(self):
        self._section_pattern = re.compile(r"""
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

    @override
    def extract_document_sections(self, text: str, project_number: str) -> List[Section]:
        return self._start_extraction(text, project_number.strip())
    

    def _start_extraction(self, text: str, project_number: str) -> List[Section]:
        sections: List[Section] = self._get_raw_sections(text)

        sections = _remove_non_valid_sections(raw_sections=sections, project_number=project_number)

        sections = _get_content_for_sections(sections, text)

        return sections

    def _get_raw_sections(self, text: str) -> List[Section]:
        raw_items: List[Section] = []
        for match in self._section_pattern.finditer(text):
            if match.group("num1"):
                number = match.group("num1") + "."
                title = match.group("title1").strip()
            else:
                number = match.group("num2")
                title = match.group("title2").strip()

            if not title:
                continue

            raw_items.append(Section(
                title=number + " " + title,
                start_pos=match.start(),
                start_content_pos=match.end()
            ))
        
        return raw_items