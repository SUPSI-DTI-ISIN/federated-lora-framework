from typing import List

from fastapi import APIRouter, status, Depends
from shared_auth_library.entities import User

from auth import jwt_validator
from schemas.institute import InstituteDTO, InstituteCreationRequestDTO, InstituteUpdateRequestDTO, InstituteTrainingParticipationDTO
from services.institute import InstituteServiceInterface, get_institute_service

router = APIRouter(prefix="/institutes")

tags = ["institute"]

@router.post(
    "",
    response_model=InstituteDTO,
    status_code=status.HTTP_201_CREATED,
    tags=tags
)
async def create_institute(
        institute_creation_request_dto: InstituteCreationRequestDTO,
        institute_service: InstituteServiceInterface = Depends(get_institute_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    return await institute_service.create_new_institute(institute_creation_request_dto=institute_creation_request_dto)

@router.put(
    "/{institute_id}",
    response_model=InstituteDTO,
    status_code=status.HTTP_201_CREATED,
    tags=tags
)
async def update_institute(
        institute_id: int,
        institute_update_request_dto: InstituteUpdateRequestDTO,
        institute_service: InstituteServiceInterface = Depends(get_institute_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    return await institute_service.update_institute(institute_id=institute_id, institute_update_request_dto=institute_update_request_dto)

@router.get(
    "",
    response_model=List[InstituteDTO],
    status_code=status.HTTP_200_OK,
    tags=tags
)
async def list_institutes(
        institute_service: InstituteServiceInterface = Depends(get_institute_service)
):
    return await institute_service.get_all()

@router.get(
    "/training-participation",
    response_model=List[InstituteTrainingParticipationDTO],
    status_code=status.HTTP_200_OK,
    tags=tags
)
async def get_institutes_training_participation(
        institute_service: InstituteServiceInterface = Depends(get_institute_service)
):
    return await institute_service.get_institutes_training_participation()

@router.get(
    "/{institute_id}",
    response_model=InstituteDTO,
    status_code=status.HTTP_200_OK,
    tags=tags
)
async def get_institute_by_id(
        institute_id: int,
        institute_service: InstituteServiceInterface = Depends(get_institute_service)
):
    return await institute_service.get_by_id(institute_id=institute_id)

@router.get(
    "/name/{institute_name}",
    response_model=InstituteDTO,
    status_code=status.HTTP_200_OK,
    tags=tags
)
async def get_institute_by_name(
        institute_name: str,
        institute_service: InstituteServiceInterface = Depends(get_institute_service)
):
    return await institute_service.get_by_name(institute_name=institute_name)

@router.delete(
    "/{institute_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=tags
)
async def delete_institute(
        institute_id: int,
        institute_service: InstituteServiceInterface = Depends(get_institute_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    await institute_service.delete_institute_by_id(institute_id=institute_id)