from fastapi import Depends

from .documents_service import DocumentsService
from .documents_service_interface import DocumentsServiceInterface
from repositories.documents import get_documents_repository, DocumentsRepositoryInterface
from config import settings

def get_documents_service(documents_repository: DocumentsRepositoryInterface = Depends(get_documents_repository)) -> DocumentsServiceInterface:
    return DocumentsService(documents_repository=documents_repository, institute_name=settings.institute_name)