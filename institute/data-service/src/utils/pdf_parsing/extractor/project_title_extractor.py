import re

from schemas.exceptions import ExtractorError


class ProjectTitleExtractor:
    _project_title_re_pattern = re.compile(r"""
                    (?m) 
                    ^                               
                    (?P<key>Title[^:\r\n]*:)\s*\r?\n\s*(?P<value>[^\r\n]+)
                    """,
                re.VERBOSE,
            )

    @classmethod
    def extract_project_title(cls, text_document: str) -> str:
        for match in cls._project_title_re_pattern.finditer(text_document):
            project_number = match.group("value").strip()
            return project_number

        raise ExtractorError(message="Cannot find any title during extraction from the text document")