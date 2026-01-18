from abc import ABC, abstractmethod
from typing import List

from schemas.documents import DocumentDTO


class DocumentsServiceInterface(ABC):
    @abstractmethod
    async def upload_data(self, file_content: bytes) -> DocumentDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[DocumentDTO]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, document_id: str) -> DocumentDTO:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, document_id: str) -> None:
        raise NotImplementedError