import re
from typing import override

from app.services.project_number_detector.base_project_number_detector import BaseProjectNumberDetector


class ProjectNumberDetector(BaseProjectNumberDetector):
    def __init__(self):
        self._project_number_pattern = re.compile(r"""
            (?m) 
            ^                               
            (?P<key>Number:)\s*\r?\n\s*(?P<value>[^\r\n]+)
            """,
            re.VERBOSE,
        )

    @override
    def extract_project_number(self, text_document: str) -> str:
        return self._manual_project_number_extraction(text_document)

    def _manual_project_number_extraction(self, text_document: str) -> str:
        for match in self._project_number_pattern.finditer(text_document):
            project_number = match.group("value").strip()
            return project_number
        return ""