from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import DocumentModel
from .documents_repository_interface import DocumentsRepositoryInterface


class DocumentsRepository(DocumentsRepositoryInterface):
    def __init__(self, db_session: AsyncSession):
        self._db_session: AsyncSession = db_session

    async def save_document(self, document_model: DocumentModel) -> DocumentModel:
        try:
            self._db_session.add(document_model)
            await self._db_session.commit()
            await self._db_session.refresh(document_model)
            return document_model
        except SQLAlchemyError as exc:
            await self._db_session.rollback()
            raise exc

    async def get_all(self) -> List[DocumentModel]:
        try:
            result = await self._db_session.execute(select(DocumentModel))
            return list(result.scalars().all())
        except SQLAlchemyError as exc:
            raise exc

    async def get_by_id(self, document_id: str) -> Optional[DocumentModel]:
        try:
            model = await self._db_session.get(DocumentModel, document_id)
            return model
        except SQLAlchemyError as exc:
            raise exc

    async def delete_document(self, document_model: DocumentModel) -> None:
        try:
            await self._db_session.delete(document_model)
            await self._db_session.commit()
        except SQLAlchemyError as exc:
            await self._db_session.rollback()
            raise exc