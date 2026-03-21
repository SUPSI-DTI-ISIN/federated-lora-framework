from contextlib import asynccontextmanager
from fastapi import FastAPI

from clients.institute.institute_node_client import InstituteNodeClient
from clients.institute.institute_node_client_interface import InstituteNodeClientInterface
from database import DatabaseConnector
from repositories.institute import InstituteRepositoryInterface, InstituteRepository
from schemas.exceptions import InstituteNameNotFoundError
from schemas.institute import InstituteCreationRequestDTO
from config import settings
from services.institute import InstituteServiceInterface, InstituteService


@asynccontextmanager
async def lifespan(app: FastAPI):
    DatabaseConnector.init_database_connection()

    await DatabaseConnector.test_connection()

    async for session in DatabaseConnector.get_db_session():
        institute_node_client: InstituteNodeClientInterface = InstituteNodeClient.get_instance()
        institute_repository = InstituteRepository(db_session=session)
        institute_service = InstituteService(institute_repository=institute_repository, institute_node_client=institute_node_client, department_realm_name=settings.realm_name)

        try:
            await institute_service.get_by_name(institute_name=settings.realm_name)
        except InstituteNameNotFoundError:
            await institute_service.create_new_institute(
                institute_creation_request_dto=InstituteCreationRequestDTO(
                    name=settings.realm_name,
                    url=settings.department_url,
                    deletable=False
                )
            )

    yield

    await DatabaseConnector.close_connection()
