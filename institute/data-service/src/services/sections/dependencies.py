from fastapi import Depends

from .sections_service import SectionsService
from .sections_service_interface import SectionsServiceInterface
from repositories.sections import get_sections_repository, SectionsRepositoryInterface

def get_sections_service(sections_repository: SectionsRepositoryInterface = Depends(get_sections_repository)) -> SectionsServiceInterface:
    return SectionsService(sections_repository=sections_repository)