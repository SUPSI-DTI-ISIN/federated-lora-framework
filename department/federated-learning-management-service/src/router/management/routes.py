from fastapi import status, Depends, APIRouter

from services.management import ManagementServiceInterface
from .dependencies import get_management_service

router = APIRouter(prefix="/management")
tags = ["federated", "management"]

@router.get(
    "/start",
    status_code=status.HTTP_200_OK,
    #response_model=FederatedDataDTO,
    tags=tags
)
async def start_federated_learning(
        management_service: ManagementServiceInterface = Depends(get_management_service)
):
    print("Start Federated Learning controller")
    await management_service.start_federated_learning()