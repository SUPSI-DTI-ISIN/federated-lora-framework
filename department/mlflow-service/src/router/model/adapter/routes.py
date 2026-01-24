from fastapi import status, Depends, HTTPException, APIRouter
from fastapi.responses import FileResponse

from schemas.model import ModelAdaptersVersionDTO, NewAdapterPathDTO, ManifestDTO
from services.adapter import AdapterRegistryServiceInterface
from .dependencies import get_adapter_registry_service

router = APIRouter(prefix="/model/{model_key}/adapters")
tags = ["model", "adapter"]

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ModelAdaptersVersionDTO,
    tags=tags
)
async def get_adapters_version(model_key: str, adapter_registry_service: AdapterRegistryServiceInterface = Depends(get_adapter_registry_service)):
    return adapter_registry_service.get_adapters_version(model_key=model_key)


@router.get(
    "/new-adapter-path",
    status_code=status.HTTP_200_OK,
    response_model=NewAdapterPathDTO,
    tags=tags
)
async def get_new_adapter_path(model_key: str, adapter_registry_service: AdapterRegistryServiceInterface = Depends(get_adapter_registry_service)):
    try:
        return adapter_registry_service.get_new_adapter_path(model_key=model_key)
    except FileNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))


@router.get(
    "/{adapter_version}/manifest",
    status_code=status.HTTP_200_OK,
    response_model=ManifestDTO,
    tags=tags
)
async def get_adapter_manifest(model_key: str, adapter_version: int, adapter_registry_service: AdapterRegistryServiceInterface = Depends(get_adapter_registry_service)):
    try:
        return adapter_registry_service.get_adapter_manifest(model_key=model_key, adapter_version=adapter_version)
    except FileNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))


@router.get(
    "/{adapter_version}/file_name/{file_name}",
    status_code=status.HTTP_200_OK,
    tags=tags
)
async def get_adapter_file(model_key: str, adapter_version: int, file_name: str, adapter_registry_service: AdapterRegistryServiceInterface = Depends(get_adapter_registry_service)):
    try:
        file_path = adapter_registry_service.get_adapter_file(
            model_key=model_key,
            adapter_version=adapter_version,
            file_name=file_name
        )

        return FileResponse(
            path=file_path,
            media_type="application/octet-stream",
            filename=file_name
        )

    except FileNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))