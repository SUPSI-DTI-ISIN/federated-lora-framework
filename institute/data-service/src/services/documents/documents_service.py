import os
import tempfile
from pathlib import Path
from typing import List

from commons.documents import ParsedDocument
from models import DocumentModel
from repositories.documents import DocumentsRepositoryInterface
from schemas.documents import DocumentDTO, TrainingSamplesDTO
from schemas.exceptions import DocumentNotFoundError, DocumentAlreadyExistsError, InvalidFileError
from utils.pdf_parsing import PdfParserService
from utils.mappers import DocumentMapper
from .documents_service_interface import DocumentsServiceInterface


class DocumentsService(DocumentsServiceInterface):
    def __init__(self, documents_repository: DocumentsRepositoryInterface, institute_name: str):
        self.__documents_repository = documents_repository
        self.__institute_name = institute_name

    async def upload_data(self, file_content: bytes, is_externally_approved: bool) -> DocumentDTO:
        if not file_content or len(file_content) == 0:
            raise InvalidFileError("File content is empty")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file_content)
            temp_path = Path(temp_file.name)

        try:
            with PdfParserService(pdf_file=temp_path) as pdf_parser:
                parsed_document: ParsedDocument = pdf_parser.get_document()

            if not parsed_document or not parsed_document.number:
                raise InvalidFileError("Invalid document data extracted from PDF")

            document = await self.__documents_repository.get_by_number(document_number=parsed_document.number)
            if document:
                raise DocumentAlreadyExistsError(document_id=document.id)

            document_model: DocumentModel = DocumentMapper.to_model(document=parsed_document)
            document_model.is_trainable = False
            document_model.is_externally_approved = is_externally_approved
            document_model_saved: DocumentModel = await self.__documents_repository.save_document(document_model=document_model)
            return DocumentDTO.model_validate(document_model_saved)
        finally:
            if temp_path.exists():
                os.remove(temp_path)

    async def get_all(self) -> List[DocumentDTO]:
        documents_model = await self.__documents_repository.get_all()
        return [DocumentDTO.model_validate(document_model) for document_model in documents_model]

    async def get_all_trainable(self, is_trainable: bool = True) -> List[DocumentDTO]:
        trainable_documents_model = await self.__documents_repository.get_all_trainable(is_trainable=is_trainable)
        return [DocumentDTO.model_validate(trainable_document_model) for trainable_document_model in trainable_documents_model]

    async def get_training_samples(self) -> TrainingSamplesDTO:
        trainable_documents_model = await self.__documents_repository.get_all_trainable(is_trainable=True)

        trainable_samples_number = sum(len(document.sections) for document in trainable_documents_model)

        return TrainingSamplesDTO(
            institute_name=self.__institute_name,
            trainable_samples_number=trainable_samples_number
        )

    async def get_by_id(self, document_id: int) -> DocumentDTO:
        document_model = await self.__documents_repository.get_by_id(document_id=document_id)
        if document_model is None:
            raise DocumentNotFoundError(document_id=document_id)

        return DocumentDTO.model_validate(document_model)

    async def update_document_trainable(self, document_id: int, is_trainable: bool) -> DocumentDTO:
        document_model = await self.__documents_repository.get_by_id(document_id=document_id)
        if document_model is None:
            raise DocumentNotFoundError(document_id=document_id)

        document_model.is_trainable = is_trainable
        updated_document_model = await self.__documents_repository.save_document(document_model=document_model)
        return DocumentDTO.model_validate(updated_document_model)

    async def update_document_externally_approved(self, document_id: int, is_externally_approved: bool) -> DocumentDTO:
        document_model = await self.__documents_repository.get_by_id(document_id=document_id)
        if document_model is None:
            raise DocumentNotFoundError(document_id=document_id)

        document_model.is_externally_approved = is_externally_approved
        updated_document_model = await self.__documents_repository.save_document(document_model=document_model)
        return DocumentDTO.model_validate(updated_document_model)

    async def delete_by_id(self, document_id: int) -> None:
        document_model = await self.__documents_repository.get_by_id(document_id=document_id)
        if document_model is None:
            raise DocumentNotFoundError(document_id=document_id)

        await self.__documents_repository.delete_document(document_model=document_model)