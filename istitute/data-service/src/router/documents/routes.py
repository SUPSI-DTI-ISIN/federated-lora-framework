from typing import List

from fastapi import APIRouter, status, UploadFile, HTTPException, Depends, File

from schemas.documents import DocumentDTO
from services import DocumentsServiceInterface
from .dependencies import get_documents_service

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
        service: DocumentsServiceInterface = Depends(get_documents_service)
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
    document_dto_saved = await service.upload_data(file_content=file_content)
    return document_dto_saved


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[DocumentDTO],
    tags=tags
)
@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[DocumentDTO],
    tags=tags
)
async def get_all(documents_service: DocumentsServiceInterface = Depends(get_documents_service)):
    return await documents_service.get_all()