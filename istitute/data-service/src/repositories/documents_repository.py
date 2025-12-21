from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import DocumentModel
from .documents_repository_interface import DocumentsRepositoryInterface


class DocumentsRepository(DocumentsRepositoryInterface):
    def __init__(self, db_session: AsyncSession):
        self._db_session: AsyncSession = db_session

    async def save_document(self, document_model: DocumentModel) -> DocumentModel:
        self._db_session.add(document_model)
        await self._db_session.commit()
        await self._db_session.refresh(document_model)
        return document_model

    async def get_all(self) -> List[DocumentModel]:
        documents_model = await self._db_session.execute(select(DocumentModel))
        return list(documents_model.scalars().all())