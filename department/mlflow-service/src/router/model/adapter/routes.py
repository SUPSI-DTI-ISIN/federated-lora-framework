from fastapi import status, Depends, HTTPException, APIRouter

from schemas.model import ModelAdaptersVersion, NewAdapterPath
from services.adapter import AdapterRegistryServiceInterface
from .dependencies import get_adapter_registry_service

router = APIRouter(prefix="/model/{model_key}")
tags = ["model", "adapter"]

@router.get(
    "/adapters",
    status_code=status.HTTP_200_OK,
    response_model=ModelAdaptersVersion,
    tags=tags
)
async def get_adapters_version(model_key: str, adapter_registry_service: AdapterRegistryServiceInterface = Depends(get_adapter_registry_service)):
    try:
        return adapter_registry_service.get_adapters_version(model_key=model_key)
    except FileNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))


@router.get(
    "/new-adapter-path",
    status_code=status.HTTP_200_OK,
    response_model=NewAdapterPath,
    tags=tags
)
async def get_new_adapter_path(model_key: str, adapter_registry_service: AdapterRegistryServiceInterface = Depends(get_adapter_registry_service)):
    try:
        return adapter_registry_service.get_new_adapter_path(model_key=model_key)
    except FileNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))