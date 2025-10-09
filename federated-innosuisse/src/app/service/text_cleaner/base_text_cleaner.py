from abc import ABC, abstractmethod


class BaseTextCleaner(ABC):
    @abstractmethod
    def clean(self, text: str) -> str:
        ...