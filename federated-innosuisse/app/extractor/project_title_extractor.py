import re

_project_title_re_pattern = re.compile(r"""
                (?m) 
                ^                               
                (?P<key>Title[^:\r\n]*:)\s*\r?\n\s*(?P<value>[^\r\n]+)
                """,
            re.VERBOSE,
        )

def extract_project_title(text_document: str) -> str:
    for match in _project_title_re_pattern.finditer(text_document):
        project_number = match.group("value").strip()
        return project_number
    return ""