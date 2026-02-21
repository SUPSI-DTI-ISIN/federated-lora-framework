from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database import DatabaseConnector
from repositories.institute import InstituteRepository, InstituteRepositoryInterface
from services.institute import InstituteService, InstituteServiceInterface


def get_institute_repository(db: AsyncSession = Depends(DatabaseConnector.get_db_session)) -> InstituteRepositoryInterface:
    return InstituteRepository(db_session=db)

def get_institute_service(institute_repository: InstituteRepositoryInterface = Depends(get_institute_repository)) -> InstituteServiceInterface:
    return InstituteService(institute_repository=institute_repository)