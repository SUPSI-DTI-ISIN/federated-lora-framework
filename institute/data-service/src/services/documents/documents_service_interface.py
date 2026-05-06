from abc import ABC, abstractmethod
from typing import List

from schemas.documents import DocumentDTO, TrainingSamplesDTO


class DocumentsServiceInterface(ABC):
    @abstractmethod
    async def upload_data(self, file_content: bytes, is_externally_approved: bool) -> DocumentDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[DocumentDTO]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_trainable(self, is_trainable: bool = True) -> List[DocumentDTO]:
        raise NotImplementedError

    @abstractmethod
    async def get_training_samples(self) -> TrainingSamplesDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, document_id: int) -> DocumentDTO:
        raise NotImplementedError

    @abstractmethod
    async def update_document_trainable(self, document_id: int, is_trainable: bool) -> DocumentDTO:
        raise NotImplementedError

    @abstractmethod
    async def update_document_externally_approved(self, document_id: int, is_externally_approved: bool) -> DocumentDTO:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, document_id: int) -> None:
        raise NotImplementedError