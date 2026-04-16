from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import DatabaseConnector
from repositories.institute import build_institute_repository
from schemas.exceptions import InstituteNameNotFoundError
from schemas.institute import InstituteCreationRequestDTO
from config import settings
from services.institute import build_institute_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    DatabaseConnector.init_database_connection()

    await DatabaseConnector.test_connection()

    async for session in DatabaseConnector.get_db_session():
        institute_repository = build_institute_repository(db=session)
        institute_service = build_institute_service(institute_repository=institute_repository)

        try:
            await institute_service.get_by_name(institute_name=settings.realm_name)
        except InstituteNameNotFoundError:
            await institute_service.create_new_institute(
                institute_creation_request_dto=InstituteCreationRequestDTO(
                    name=settings.realm_name,
                    url=settings.department_url,
                    deletable=False,
                    updatable=False
                )
        )

    yield

    await DatabaseConnector.close_connection()
