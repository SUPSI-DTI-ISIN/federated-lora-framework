import os
import tempfile
from pathlib import Path
from typing import List

from models import DocumentModel
from repositories import DocumentsRepositoryInterface
from schemas.documents import DocumentDTO
from utils.pdf_parsing import PdfParserService
from utils.mappers import DocumentMapper
from .documents_service_interface import DocumentsServiceInterface


class DocumentsService(DocumentsServiceInterface):
    def __init__(self, documents_repository: DocumentsRepositoryInterface):
        self._documents_repository: DocumentsRepositoryInterface = documents_repository

    async def upload_data(self, file_content: bytes) -> DocumentDTO:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file_content)
            temp_path = Path(temp_file.name)

        try:
            with PdfParserService(pdf_file=temp_path) as pdf_parser:
                document_dto: DocumentDTO = pdf_parser.get_document()
            document_model: DocumentModel = DocumentMapper.to_model(dto=document_dto)
            document_model_saved: DocumentModel = await self._documents_repository.save_document(document_model=document_model)
            return DocumentDTO.model_validate(document_model_saved)
        finally:
            if temp_path.exists():
                os.remove(temp_path)

    async def get_all(self) -> List[DocumentDTO]:
        documents = await self._documents_repository.get_all()
        return [DocumentDTO.model_validate(document) for document in documents]