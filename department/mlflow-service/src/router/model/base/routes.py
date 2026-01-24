from fastapi import status, Depends, HTTPException, APIRouter
from fastapi.responses import FileResponse

from .dependencies import get_model_registry_service
from schemas.model import ModelManifestDTO
from services.model import ModelRegistryServiceInterface

router = APIRouter(prefix="/model/{model_key}")
tags = ["model", "base"]

@router.get(
    "/manifest",
    status_code=status.HTTP_200_OK,
    response_model=ModelManifestDTO,
    tags=tags
)
async def get_model_base_manifest(model_key: str, model_registry_service: ModelRegistryServiceInterface = Depends(get_model_registry_service)):
    try:
        return model_registry_service.get_model_manifest(model_key=model_key)
    except FileNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))


@router.get(
    "/file_name/{file_name}",
    status_code=status.HTTP_200_OK,
    tags=tags
)
async def get_model_base_file(model_key: str, file_name: str, model_registry_service: ModelRegistryServiceInterface = Depends(get_model_registry_service)):
    try:
        file_path = model_registry_service.get_model_file(
            model_key=model_key,
            file_name=file_name
        )

        return FileResponse(
            path=file_path,
            media_type="application/octet-stream",
            filename=file_name
        )

    except FileNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))
