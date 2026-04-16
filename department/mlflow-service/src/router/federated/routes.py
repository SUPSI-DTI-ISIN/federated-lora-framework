from fastapi import status, Depends, HTTPException, APIRouter

from services.adapter import AdapterRegistryServiceInterface, get_adapter_registry_service
from schemas.model import FederatedDataDTO
from services.model import ModelRegistryServiceInterface, get_model_registry_service

router = APIRouter(prefix="/federated/{model_key}")
tags = ["federated"]

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=FederatedDataDTO,
    tags=tags
)
async def get_federated_data(model_key: str, model_registry_service: ModelRegistryServiceInterface = Depends(get_model_registry_service), adapter_registry_service: AdapterRegistryServiceInterface = Depends(get_adapter_registry_service)):
    try:
        model_base_path = model_registry_service.get_model_path(model_key=model_key)
        new_adapter_path = adapter_registry_service.get_new_adapter_path(model_key=model_key)
        latest_adapter_path = adapter_registry_service.get_latest_adapter_path(model_key=model_key)

        return FederatedDataDTO(
            model_path=model_base_path,
            new_adapter_path=new_adapter_path,
            latest_adapter_path=latest_adapter_path
        )
    except FileNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))