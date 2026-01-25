from typing import Optional

from fastapi import status, Depends, APIRouter, HTTPException

from schemas.model import ModelPathDTO
from services.model_path import ModelPathServiceInterface
from .dependencies import get_model_path_service

router = APIRouter(prefix="/model/{model_key}/path")
tags = ["path"]

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ModelPathDTO,
    tags=tags
)
async def get_model_path_for_inference(model_key: str, adapter_version: Optional[int] = None, model_path_service: ModelPathServiceInterface = Depends(get_model_path_service)):
    try:
        return model_path_service.get_model_path_for_inference(model_key=model_key, adapter_version=adapter_version)
    except FileNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))