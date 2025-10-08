import re
from pymupdf import Page
from typing import List, Optional, override
from app.model.section import Section
from app.service.ollama.ollama_service import OllamaService
from app.service.section.base_section_detector import ISectionDetector

SYSTEM_PROMPT = """
You are a deterministic extractor of numbered hierarchical section headings from documents. Your task is to identify only section headings that strictly match numeric patterns like "1.", "1.1", "1.1.1", etc. Follow these rules strictly.

Language handling:
- Automatically detect the language of the input document. Use that detected language for **all textual output inside the JSON fields `title`**. Do NOT translate those fields: return them verbatim (trimmed) in the original language and preserve Unicode diacritics and script.
- If the document contains multiple languages, detect the language at the section-level: use the language of each section heading (or the language most clearly associated with that section) for that section's `title`.
- If language detection fails or confidence is very low, default to English as a fallback. In that case, still produce the JSON but ensure confidence scores reflect low detection confidence.
- JSON keys must remain in English exactly as specified (`number`, `title`, `level`, `parent_number`). Only the *value* for `title` follow the document language.
- Normalize textual values using Unicode NFC before returning them, to keep diacritics consistent.
- Support non-Latin scripts: treat numerals and punctuation in the document's script appropriately when recognizing headings. (If numerals are in non-Western digit systems, attempt to interpret them as numbers; if uncertain, do not mark as a section.)

Recognition rules:
1. Valid numeric pattern: a line qualifies if it begins with an integer followed by zero or more groups of ".<number>" (examples: "1.", "2.1", "3.2.1"). Allowed separator immediately after a number is "." or a space (example: "1. Title", "1.1 Title").
2. Exclude candidates that are clearly numeric data/identifiers (e.g., long decimal numbers such as "102.518", version codes, timestamps, project numbers present in the header repeated across pages).
3. Depth: accept multi-level numbering (e.g., 1.1.1) but discard if any numeric part is unusually long (> 4 characters) unless the document consistently uses long numeric parts.
4. For each candidate line compute a confidence score (0.0–1.0) based on adherence to the patterns above and language-aware heuristics (e.g., if the token to the right is natural-language text in the detected language, increase confidence).
5. Be conservative: only mark as a valid section when confidence is high. If confidence is low or ambiguous, do not mark the line as a section.

Output required:
- **Return ONLY** a JSON array (no extra text, explanation or markup) containing identified valid sections. Each section object must include:
  - `number` (string): the numeric section's identifier found (e.g., "1", "1.1", "2.3.1").
  - `title` (string): the text to the right of the number, trimmed; returned in the original language of the section.
  - `level` (int): the section level (e.g., "1." -> 1; "1.1" -> 2; "1.1.1" -> 3).
  - `parent_number` (Optional[str]): numeric token of the parent section (e.g., "1" for "1.1"; "2.1" for "2.1.3"); `null` if none.

Formatting:
- Return valid JSON only. Order objects by ascending `number`.
- If no candidates, return `[]`.

Strict: do not include any extra text outside the JSON array.
"""


class SectionDetector(ISectionDetector):
    def __init__(self):
        self._ollama_service = OllamaService()
        self._section_pattern = re.compile(
            r'^(\d+(?:\.\d+)*)\s+([^\n]+?)(?:\n|$)',
            re.MULTILINE
        )

    @override
    def detect_sections(self, text: str) -> List[Section]:
        return self._ollama_service.generate_document_sections(system_prompt=SYSTEM_PROMPT, user_prompt=text)
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
            