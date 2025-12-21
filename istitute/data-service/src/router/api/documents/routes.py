from fastapi import APIRouter, status, UploadFile, HTTPException

router = APIRouter(prefix="/documents")

tags = ["documents"]

@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    tags=tags
)
async def upload(file: UploadFile):
    if not any(file.filename.endswith(ext) for ext in ['.pdf', '.docx']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files allowed"
        )

    content = await file.read()
    #result = await service.process_and_store(content, file.filename)
    
    return {}
