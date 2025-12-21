from repositories.documents import DocumentsRepositoryInterface
from .documents_service_interface import DocumentsServiceInterface


class DocumentsService(DocumentsServiceInterface):
    def __init__(self, documents_repository: DocumentsRepositoryInterface):
        self._documents_repository: DocumentsRepositoryInterface = documents_repository

    async def upload_data(self) -> None:
        return None

    async def get_all(self) -> None:
        return await self._documents_repository.get_all()