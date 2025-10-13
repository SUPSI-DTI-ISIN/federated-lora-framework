import re
from typing import override
from app.service.text_cleaner.strategies.base_text_cleaner import BaseTextCleaner


class PageNumberCleaner(BaseTextCleaner):
    def __init__(self):
        self._replace_with = ""
        self._pattern = re.compile(
            r'\b\d+\s*/\s*\d+\b',
            re.MULTILINE
        )
    
    @override
    def clean(self, text: str) -> str:
        return self._pattern.sub(self._replace_with, text)

