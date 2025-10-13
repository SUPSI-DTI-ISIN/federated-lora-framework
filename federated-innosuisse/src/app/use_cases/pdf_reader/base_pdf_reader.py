from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from app.model.document import Document


class BasePdfReader(ABC):
    @abstractmethod
    def parse_folder(self, folder_path: Path) -> List[Document]:
        ...