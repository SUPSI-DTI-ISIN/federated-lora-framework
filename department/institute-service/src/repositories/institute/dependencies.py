from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .institute_repository_interface import InstituteRepositoryInterface
from .institute_repository import InstituteRepository
from database import get_db_session

def get_institute_repository(db: AsyncSession = Depends(get_db_session)) -> InstituteRepositoryInterface:
    return InstituteRepository(db_session=db)

def build_institute_repository(db: AsyncSession) -> InstituteRepositoryInterface:
    return InstituteRepository(db_session=db)