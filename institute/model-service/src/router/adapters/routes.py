from fastapi import status, Depends, APIRouter
from shared_auth_library.entities import User

from auth import jwt_validator
from schemas.model import AvailableAdaptersDTO, NewAdapterRequestDTO, AdapterDTO
from services.adapter import AdapterRegistryServiceInterface
from .dependencies import get_adapter_registry_service

router = APIRouter(prefix="/models/{model_key}/adapters")
tags = ["adapters"]

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=AvailableAdaptersDTO,
    tags=tags
)
async def get_available_adapters(
        model_key: str,
        adapter_registry_service: AdapterRegistryServiceInterface = Depends(get_adapter_registry_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    return adapter_registry_service.get_available_adapters(model_key=model_key)

@router.get(
    "/local",
    status_code=status.HTTP_200_OK,
    response_model=AvailableAdaptersDTO,
    tags=tags
)
async def get_available_local_adapters(
        model_key: str, adapter_registry_service: AdapterRegistryServiceInterface = Depends(get_adapter_registry_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    return adapter_registry_service.get_available_local_adapters(model_key=model_key)

@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=AdapterDTO,
    tags=tags
)
async def save_new_adapter(
        model_key: str,
        new_adapter_request_dto: NewAdapterRequestDTO,
        adapter_registry_service: AdapterRegistryServiceInterface = Depends(get_adapter_registry_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    return adapter_registry_service.download_remote_adapter(model_key=model_key, adapter_version=new_adapter_request_dto.version)