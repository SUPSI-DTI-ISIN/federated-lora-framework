from fastapi import APIRouter, status, UploadFile, HTTPException

router = APIRouter()

tags = ["health"]

@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    tags=tags
)
async def health():
    return {"status": "healthy"}
