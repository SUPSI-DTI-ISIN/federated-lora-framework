from fastapi import status, Depends, APIRouter, HTTPException

from schemas.model import AvailableAdaptersDTO, NewAdapterRequestDTO, AdapterDTO, ModelPathDTO
from services.adapter import AdapterRegistryServiceInterface
from .dependencies import get_adapter_registry_service

router = APIRouter(prefix="/model/{model_key}/adapters")
tags = ["adapters"]

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=AvailableAdaptersDTO,
    tags=tags
)
async def get_available_adapters(model_key: str, adapter_registry_service: AdapterRegistryServiceInterface = Depends(get_adapter_registry_service)):
    return adapter_registry_service.get_available_adapters(model_key=model_key)


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=AdapterDTO,
    tags=tags
)
async def save_new_adapter(model_key: str, new_adapter_request_dto: NewAdapterRequestDTO, adapter_registry_service: AdapterRegistryServiceInterface = Depends(get_adapter_registry_service)):
    return adapter_registry_service.download_remote_adapter(model_key=model_key, adapter_version=new_adapter_request_dto.version)


@router.get(
    "/{adapter_version}",
    status_code=status.HTTP_200_OK,
    response_model=ModelPathDTO,
    tags=tags
)
async def get_model_path_for_adapter(model_key: str, adapter_version: int, adapter_registry_service: AdapterRegistryServiceInterface = Depends(get_adapter_registry_service)):
    try:
        return adapter_registry_service.get_model_path_for_adapter(model_key=model_key, adapter_version=adapter_version)
    except FileNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))