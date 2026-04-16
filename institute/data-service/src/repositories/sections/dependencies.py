from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from .sections_repository import SectionsRepository
from .sections_repository_interface import SectionsRepositoryInterface
from database import get_db_session

def get_sections_repository(db: AsyncSession = Depends(get_db_session)) -> SectionsRepositoryInterface:
    return SectionsRepository(db_session=db)