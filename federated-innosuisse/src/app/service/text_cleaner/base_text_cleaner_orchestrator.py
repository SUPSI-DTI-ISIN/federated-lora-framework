from abc import ABC, abstractmethod
from app.service.text_cleaner.strategies.base_text_cleaner import BaseTextCleaner

class BaseTextCleanerOrchestrator(ABC):
    @abstractmethod
    def register_cleaner(self, cleaner: BaseTextCleaner) -> None:
        ...
    
    @abstractmethod
    def remove_all_cleaners(self) -> None:
        ...

    @abstractmethod
    def clean(self, text: str) -> str:
        ...