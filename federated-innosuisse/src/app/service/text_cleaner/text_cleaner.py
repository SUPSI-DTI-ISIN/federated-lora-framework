from typing import List, Optional, override
from app.service.text_cleaner.base_text_cleaner import BaseTextCleaner


class TextCleaner(BaseTextCleaner):
    def __init__(self, cleaners: Optional[List[BaseTextCleaner]] = None):
        self._cleaners: List[BaseTextCleaner] = list(cleaners) if cleaners else []

    def register_cleaner(self, cleaner: BaseTextCleaner) -> None:
        self._cleaners.append(cleaner)
    
    def remove_all_cleaners(self) -> None:
        self._cleaners.clear()

    @override
    def clean(self, text: str) -> str:
        for cleaner in self._cleaners:
            text = cleaner.clean(text)
        return text
    