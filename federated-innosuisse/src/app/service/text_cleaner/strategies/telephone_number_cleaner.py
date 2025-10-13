import re
from typing import override
from app.service.text_cleaner.strategies.base_text_cleaner import BaseTextCleaner


class TelephoneNumberCleaner(BaseTextCleaner):
    def __init__(self):
        self._replace_with = ""
        self._pattern = re.compile(
            r'(?<!\w)\+(?:\d[\d\s().-]{4,20}\d)(?!\w)',
            re.MULTILINE
        )

    @override
    def clean(self, text: str) -> str:
        return self._pattern.sub(self._replace_with, text)
