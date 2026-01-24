from fastapi import status, Depends, APIRouter

from schemas.model import AvailableAdaptersDTO
from services.adapter import AdapterRegistryServiceInterface
from .dependencies import get_adapter_registry_service

router = APIRouter(prefix="/model/{model_key}")
tags = ["adapters"]

@router.get(
    "/adapters",
    status_code=status.HTTP_200_OK,
    response_model=AvailableAdaptersDTO,
    tags=tags
)
async def get_available_adapters(model_key: str, adapter_registry_service: AdapterRegistryServiceInterface = Depends(get_adapter_registry_service)):
    return adapter_registry_service.get_available_adapters(model_key=model_key)