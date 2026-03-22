from fastapi import APIRouter, status, Depends
from shared_auth_library.entities import User

from auth import jwt_validator
from schemas.documents import SectionDTO, UpdateSectionRequestDTO
from services.sections import SectionsServiceInterface
from .dependencies import get_sections_service

router = APIRouter(prefix="/sections")

tags = ["sections"]


@router.delete(
    "/{section_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=tags
)
async def delete_section_by_id(
        section_id: int,
        service: SectionsServiceInterface = Depends(get_sections_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    await service.delete_by_id(section_id=section_id)

@router.put(
    "/{section_id}",
    status_code=status.HTTP_200_OK,
    response_model=SectionDTO,
    tags=tags
)
async def update_section(
        section_id: int,
        update_section_content_request_dto: UpdateSectionRequestDTO,
        service: SectionsServiceInterface = Depends(get_sections_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    return await service.update_section_content(section_id=section_id, update_section_content_request_dto=update_section_content_request_dto)