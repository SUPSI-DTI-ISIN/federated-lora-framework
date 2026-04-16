from typing import List

from fastapi import APIRouter, status, UploadFile, HTTPException, Depends, File
from shared_auth_library.entities import User

from auth import jwt_validator
from schemas.documents import DocumentDTO, UpdateDocumentTrainableRequestDTO, TrainingSamplesDTO
from services.documents import DocumentsServiceInterface, get_documents_service

router = APIRouter(prefix="/documents")

tags = ["documents"]

@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=DocumentDTO,
    tags=tags
)
async def upload(
        file: UploadFile = File(..., description="PDF file to upload"),
        service: DocumentsServiceInterface = Depends(get_documents_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )

    file_content = await file.read()
    return await service.upload_data(file_content=file_content)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[DocumentDTO],
    tags=tags
)
async def get_all(
        documents_service: DocumentsServiceInterface = Depends(get_documents_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    return await documents_service.get_all()

@router.get(
    "/trainable",
    status_code=status.HTTP_200_OK,
    response_model=List[DocumentDTO],
    tags=tags
)
async def get_all_trainable(
        documents_service: DocumentsServiceInterface = Depends(get_documents_service),
        #_: User = Depends(jwt_validator.get_current_user_required)
):
    return await documents_service.get_all_trainable()

@router.get(
    "/training-samples",
    status_code=status.HTTP_200_OK,
    response_model=TrainingSamplesDTO,
    tags=tags
)
async def get_training_samples(
        documents_service: DocumentsServiceInterface = Depends(get_documents_service),
        #_: User = Depends(jwt_validator.get_current_user_required)
):
    return await documents_service.get_training_samples()

@router.get(
    "/{document_id}",
    status_code=status.HTTP_200_OK,
    response_model=DocumentDTO,
    tags=tags
)
async def get_by_id(
        document_id: int,
        service: DocumentsServiceInterface = Depends(get_documents_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    return await service.get_by_id(document_id=document_id)

@router.put(
    "/{document_id}",
    status_code=status.HTTP_200_OK,
    response_model=DocumentDTO,
    tags=tags
)
async def update_document_trainable(
        document_id: int,
        update_document_trainable_request_dto: UpdateDocumentTrainableRequestDTO,
        service: DocumentsServiceInterface = Depends(get_documents_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    return await service.update_document_trainable(document_id=document_id, is_trainable=update_document_trainable_request_dto.is_trainable)


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=tags
)
async def delete_by_id(
        document_id: int,
        service: DocumentsServiceInterface = Depends(get_documents_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    await service.delete_by_id(document_id=document_id)