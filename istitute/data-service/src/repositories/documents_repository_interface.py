from abc import ABC, abstractmethod
from typing import List

from models import DocumentModel


class DocumentsRepositoryInterface(ABC):
    @abstractmethod
    async def save_document(self, document_model: DocumentModel) -> DocumentModel:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[DocumentModel]:
        raise NotImplementedError