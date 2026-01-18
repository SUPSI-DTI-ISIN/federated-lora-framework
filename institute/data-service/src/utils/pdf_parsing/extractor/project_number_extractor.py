import re

from schemas.exceptions import ExtractorError


class ProjectNumberExtractor:
    _project_number_re_pattern = re.compile(r"""
                (?m) 
                ^                               
                (?P<key>Number:)\s*\r?\n\s*(?P<value>[^\r\n]+)
                """,
                re.VERBOSE,
            )

    @classmethod
    def extract_project_number(cls, text_document: str) -> str:
        for match in cls._project_number_re_pattern.finditer(text_document):
            project_number = match.group("value").strip()
            return project_number

        raise ExtractorError(message="Cannot find any project number during extraction from the text document")