from typing import List, Optional, override
from app.service.text_cleaner.strategies.base_text_cleaner import BaseTextCleaner
from app.service.text_cleaner.base_text_cleaner_orchestrator import BaseTextCleanerOrchestrator


class TextCleanerOrchestrator(BaseTextCleanerOrchestrator):
    def __init__(self, cleaners: Optional[List[BaseTextCleaner]] = None):
        self._cleaners: List[BaseTextCleaner] = list(cleaners) if cleaners else []

    @override
    def register_cleaner(self, cleaner: BaseTextCleaner) -> None:
        self._cleaners.append(cleaner)
    
    @override
    def remove_all_cleaners(self) -> None:
        self._cleaners.clear()

    @override
    def clean(self, text: str) -> str:
        for cleaner in self._cleaners:
            text = cleaner.clean(text)
        return text
    