from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from pymupdf import Page

class BasePdfParser(ABC):
    @abstractmethod
    def load(self, path: Path) -> None: 
        ...
    
    @abstractmethod
    def get_all_text_document(self) -> str:
        ...
    
    @abstractmethod
    def get_pages(self) -> List[Page]:
        ...
    
    @abstractmethod
    def close(self) -> None:
        ...
    