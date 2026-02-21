from typing import List

from fastapi import APIRouter, status, Depends

from schemas.institute import InstituteDTO, InstituteCreationRequestDTO
from services.institute import InstituteServiceInterface
from .dependencies import get_institute_service

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
):
    return await institute_service.create_new_institute(institute_creation_request_dto=institute_creation_request_dto)


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

@router.delete(
    "/{institute_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=tags
)
async def delete_institute(
        institute_id: int,
        institute_service: InstituteServiceInterface = Depends(get_institute_service)
):
    await institute_service.delete_institute_by_id(institute_id=institute_id)