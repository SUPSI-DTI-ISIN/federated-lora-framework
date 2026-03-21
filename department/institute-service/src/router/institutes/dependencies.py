from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from clients.institute.institute_node_client import InstituteNodeClient
from clients.institute.institute_node_client_interface import InstituteNodeClientInterface
from config import settings
from database import DatabaseConnector
from repositories.institute import InstituteRepository, InstituteRepositoryInterface
from services.institute import InstituteService, InstituteServiceInterface


def get_institute_repository(db: AsyncSession = Depends(DatabaseConnector.get_db_session)) -> InstituteRepositoryInterface:
    return InstituteRepository(db_session=db)

def get_institute_node_client() -> InstituteNodeClientInterface:
    return InstituteNodeClient.get_instance()

def get_institute_service(institute_repository: InstituteRepositoryInterface = Depends(get_institute_repository), institute_node_client: InstituteNodeClientInterface = Depends(get_institute_node_client), department_realm_name: str = settings.realm_name) -> InstituteServiceInterface:
    return InstituteService(institute_repository=institute_repository, institute_node_client=institute_node_client, department_realm_name=department_realm_name)