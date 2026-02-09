from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import DatabaseConnector
from repositories.sections import SectionsRepositoryInterface, SectionsRepository
from services.sections import SectionsServiceInterface, SectionsService

def get_sections_repository(db: AsyncSession = Depends(DatabaseConnector.get_db_session)) -> SectionsRepositoryInterface:
    return SectionsRepository(db_session=db)

def get_sections_service(sections_repository: SectionsRepositoryInterface = Depends(get_sections_repository)) -> SectionsServiceInterface:
    return SectionsService(sections_repository=sections_repository)