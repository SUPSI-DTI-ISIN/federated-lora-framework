from fastapi import status, Depends, APIRouter
from shared_auth_library.entities import User

from auth import jwt_validator
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
        management_service: ManagementServiceInterface = Depends(get_management_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    print("Start Federated Learning controller")
    await management_service.start_federated_learning()