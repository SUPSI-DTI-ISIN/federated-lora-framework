
from abc import ABC, abstractmethod


class BaseParser(ABC):
    @abstractmethod
    def load(self, path: str) -> None: 
        ...
    
    @abstractmethod
    def get_pages(self) -> int:
        ...
    
    @abstractmethod
    def close(self) -> None:
        ...
    