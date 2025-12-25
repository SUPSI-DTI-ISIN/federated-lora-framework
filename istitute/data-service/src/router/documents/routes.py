from typing import List

from fastapi import APIRouter, status, UploadFile, HTTPException, Depends, File, Path

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
    return await service.upload_data(file_content=file_content)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[DocumentDTO],
    tags=tags
)
async def get_all(documents_service: DocumentsServiceInterface = Depends(get_documents_service)):
    return await documents_service.get_all()


@router.get(
    "/{document_id}",
    status_code=status.HTTP_200_OK,
    response_model=DocumentDTO,
    tags=tags
)
async def get_by_id(
        document_id: str = Path(..., description="Document id", min_length=1, max_length=50),
        service: DocumentsServiceInterface = Depends(get_documents_service)
):
    return await service.get_by_id(document_id=document_id)



@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=tags
)
async def delete_by_id(
        document_id: str = Path(..., description="Document id", min_length=1, max_length=50),
        service: DocumentsServiceInterface = Depends(get_documents_service)
):
    await service.delete_by_id(document_id=document_id)