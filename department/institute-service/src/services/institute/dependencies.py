from fastapi import Depends

from .institute_service import InstituteService
from .institute_service_interface import InstituteServiceInterface
from repositories.institute import InstituteRepositoryInterface, get_institute_repository, build_institute_repository
from clients.institute import InstituteNodeClientInterface, get_institute_node_client
from config import settings

def get_institute_service(institute_repository: InstituteRepositoryInterface = Depends(get_institute_repository), institute_node_client: InstituteNodeClientInterface = Depends(get_institute_node_client), department_realm_name: str = settings.realm_name) -> InstituteServiceInterface:
    return InstituteService(institute_repository=institute_repository, institute_node_client=institute_node_client, department_realm_name=department_realm_name)

def build_institute_service(institute_repository: InstituteRepositoryInterface, institute_node_client: InstituteNodeClientInterface = get_institute_node_client(), department_realm_name: str = settings.realm_name) -> InstituteServiceInterface:
    return InstituteService(institute_repository=institute_repository, institute_node_client=institute_node_client, department_realm_name=department_realm_name)