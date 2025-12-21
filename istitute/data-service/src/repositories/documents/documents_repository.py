from sqlalchemy.ext.asyncio import AsyncSession

from .documents_repository_interface import DocumentsRepositoryInterface


class DocumentsRepository(DocumentsRepositoryInterface):
    def __init__(self, db_session: AsyncSession):
        self._db_session: AsyncSession = db_session

    async def get_all(self) -> None:
        return None