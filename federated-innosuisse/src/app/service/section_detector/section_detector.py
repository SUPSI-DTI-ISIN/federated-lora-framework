import json
import re
from pymupdf import Page
from typing import List, Optional, Tuple, override
from app.model.section import Section
from app.service.ollama.ollama_service import OllamaService
from app.service.section_detector.base_section_detector import BaseSectionDetector

def build_system_prompt(project_number: str) -> str:
    return f"""
You are a deterministic extractor of numbered hierarchical section headings from documents. Your task is to identify and extract only section that strictly match numeric patterns like "1. <title>", "1.1 <title>", "1.1.1 <title>".

FOLLOW THESE RULES STRICTLY.

Language handling:
- Automatically detect the language of the input document. Use that detected language for **all textual output inside the JSON field `title`**.
- If the document contains multiple languages, detect the language at the section-level: use the language of each section heading (or the language most clearly associated with that section) for that section's `title`.
- If language detection fails or confidence is very low, default to English as a fallback.
- JSON keys must remain in English exactly as specified (`number`, `title`, `level`, `parent_number`). Only the *value* for `title` follow the document language.

Recognition and Extraction rules:
Given the text of a PDF document as input, you must identify and extract ONLY the section indices with a specific pattern. In the provided text, there may be no valid sections to recognize and extract; in that case, you must return an empty list [].
To recognize a section, you must identify two components which they MUST be together:
The first part: a number indicating the indexed reference (e.g. "1.", "1.1", "1.1.1", etc.);
The second part: the title assigned to that section (e.g. in "1.1 Test Section Recognition and Extraction", the first part is "1.1" and the second part is "Test Section Recognition and Extraction").
If only one of the two parts is present in the text (i.e., only the first or only the second), it is not considered a valid indexed section and must be ignored.
The first part of a section must always be a number, and each number in the sequence must be separated only by dots (.).
If the index is a first-level index (e.g. "1."), the dot (.) is still present even without following number, and it represents the root index within the indexed hierarchy.
Any separators characters between the first numerical part and the second textual part can be only the dot character '.'
If any line in the text at least contains (not necessarily exactly matches) the value {project_number}, you MUST ignore it.


Output required:
- **Return ONLY** a JSON array (no extra text, explanation or markup) containing identified valid sections. Each section object must include:
  - `number` (string): the numeric section's identifier found (e.g., "1. <title>" -> "1.", "1.1 <title>" -> "1.1", "2.3.1 <title>" -> "2.3.1").
  - `title` (string): the text on the right of the number, trimmed; returned in the original language of the section (e.g., "1. <title>" -> "<title>").
  - `level` (int): the section level of the tree (e.g., "1. <title>" -> 1; "1.1 <title>" -> 2; "1.1.1 <title>" -> 3; "4.1 <title>" -> 2).

Formatting:
- Return valid JSON only. Order objects by ascending `number`.
- If no candidates, return `[]`.

Strict: do not include any extra text outside the JSON array. 
"""

class SectionDetector(BaseSectionDetector):
    def __init__(self):
        self._ollama_service = OllamaService()
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
    def detect_sections(self, text: str, project_number: str) -> List[Section]:
        print(text)
        #return self._ollama_service.call_model(system_prompt=build_system_prompt(project_number), user_prompt=text)
        return self._extract_sections(text, project_number.strip())
    

    def _extract_sections(self, text: str, project_number: str) -> List[str]:
        sections: List[Section] = self._get_raw_items(text)

        sections = self._remove_non_valid_sections(raw_sections=sections, project_number=project_number)

        sections = self._get_content_for_sections(sections, text)
        
        for section in sections:
            print(json.dumps(section.to_dict(), indent=4))
        return []

    def _get_raw_items(self, text: str) -> List[Section]:
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

    def _remove_non_valid_sections(self, raw_sections: List[Section], project_number: str) -> List[Section]:
        items_counter = dict()

        for item in raw_sections:
            items_counter[item.title] = items_counter.get(item.title, 0) + 1

        result: List[Section] = []

        for item in raw_sections:
            if items_counter.get(item.title, 0) == 1 and project_number not in item.title:
                result.append(item)
        
        return result

    def _get_content_for_sections(self, sections: List[Section], text: str) -> List[Section]:
        result: List[Section] = []

        for index, section in enumerate(sections):
            start = section.start_content_pos
            end = sections[index + 1].start_pos if index + 1 < len(sections) else len(text)
            content = text[start:end].strip()
            section.content = content
            result.append(section)

        return result