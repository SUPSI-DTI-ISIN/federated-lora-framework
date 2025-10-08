
from abc import ABC, abstractmethod
from typing import Dict, List
from pymupdf import Page

class BaseParser(ABC):
    @abstractmethod
    def load(self, path: str) -> None: 
        ...
    
    @abstractmethod
    def get_text_document(self) -> str:
        ...
    
    @abstractmethod
    def get_pages(self) -> List[Page]:
        ...
    
    @abstractmethod
    def close(self) -> None:
        ...
    