from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import DatabaseConnector
from repositories import DocumentsRepositoryInterface, DocumentsRepository
from services import DocumentsServiceInterface, DocumentsService

def get_documents_repository(db: AsyncSession = Depends(DatabaseConnector.get_db_session)) -> DocumentsRepositoryInterface:
    return DocumentsRepository(db_session=db)

def get_documents_service(documents_repository: DocumentsRepositoryInterface = Depends(get_documents_repository)) -> DocumentsServiceInterface:
    return DocumentsService(documents_repository=documents_repository)