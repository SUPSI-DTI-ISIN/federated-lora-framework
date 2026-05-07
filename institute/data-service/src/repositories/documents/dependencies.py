from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from .documents_repository import DocumentsRepository
from .documents_repository_interface import DocumentsRepositoryInterface
from database import get_db_session

def get_documents_repository(db: AsyncSession = Depends(get_db_session)) -> DocumentsRepositoryInterface:
    return DocumentsRepository(db_session=db)