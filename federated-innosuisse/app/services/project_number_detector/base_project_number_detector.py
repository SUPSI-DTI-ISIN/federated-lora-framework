from abc import ABC, abstractmethod


class BaseProjectNumberDetector(ABC):
    @abstractmethod
    def extract_project_number(self, text_document: str) -> str:
        ...