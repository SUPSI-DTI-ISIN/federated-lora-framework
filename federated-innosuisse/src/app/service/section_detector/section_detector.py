import re
from pymupdf import Page
from typing import List, Optional, override
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
        self._section_pattern = re.compile(
            r'^(\d+(?:\.\d+)*)\s+([^\n]+?)(?:\n|$)',
            re.MULTILINE
        )

    @override
    def detect_sections(self, text: str, project_number: str) -> List[Section]:
        print(text)
        return self._ollama_service.call_model(system_prompt=build_system_prompt(project_number), user_prompt=text)
        #return self._manual_script_extraction(text_document)
    
    def _manual_script_extraction(self, text_document: str) -> List[Section]:
        sections: List[Section] = []

        for match in self._section_pattern.finditer(text_document):
            section_number = match.group(1)
            section_title = match.group(2).strip()
            start_content_pos = match.end()
            section_level = section_number.count('.')
            parent_number = self._get_parent_number(section_number)
            
            section: Section = Section(
                number=section_number,
                title=section_title,
                level=section_level,
                start_content_pos=start_content_pos,
                parent_number=parent_number
            )

            sections.append(section)
        
        sections = self._build_sections_content(sections, text_document)

        return sections
    
    def _get_parent_number(self, section_number: str) -> Optional[str]:
        parts = section_number.split('.')
        if len(parts) == 1:
            return None
        return '.'.join(parts[:-1])
    
    def _build_sections_content(self, sections: List[Section], text_document: str) -> List[Section]:
        for i, section in enumerate(sections):
            start_text = section.start_content_pos
            end_text = (sections[i + 1].start_content_pos 
                   if i + 1 < len(sections) 
                   else len(text_document))
            
            content = text_document[start_text:end_text]
            section.content = content
        
        return sections
            