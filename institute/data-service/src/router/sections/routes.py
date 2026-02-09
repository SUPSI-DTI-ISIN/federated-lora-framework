from fastapi import APIRouter, status, Depends
from shared_auth_library.entities import User

from auth import jwt_validator
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