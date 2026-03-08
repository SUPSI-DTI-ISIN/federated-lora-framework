from typing import List

from entities import InstituteModel
from repositories.institute import InstituteRepositoryInterface
from schemas.institute import InstituteDTO, InstituteCreationRequestDTO, InstituteUpdateRequestDTO
from schemas.exceptions import InstituteNotFoundError, InstituteNameNotFoundError, InstituteCannotBeDeletedError
from .institute_service_interface import InstituteServiceInterface


class InstituteService(InstituteServiceInterface):
    def __init__(self, institute_repository: InstituteRepositoryInterface):
        self.__institute_repository = institute_repository

    async def create_new_institute(self, institute_creation_request_dto: InstituteCreationRequestDTO) -> InstituteDTO:
        new_institute = InstituteModel(
            name=institute_creation_request_dto.name,
            url=institute_creation_request_dto.url,
            deletable=institute_creation_request_dto.deletable
        )

        new_institute_created = await self.__institute_repository.save(institute_model=new_institute)
        return InstituteDTO.model_validate(new_institute_created)

    async def update_institute(self, institute_id: int, institute_update_request_dto: InstituteUpdateRequestDTO) -> InstituteDTO:
        institute = await self.__institute_repository.get_by_id(institute_id=institute_id)

        if institute is None:
            raise InstituteNotFoundError(institute_id=institute_id)

        institute.name = institute_update_request_dto.name if institute_update_request_dto.name is not None else institute.name
        institute.url = institute_update_request_dto.url if institute_update_request_dto.url is not None else institute.url

        updated_institute = await self.__institute_repository.save(institute_model=institute)
        return InstituteDTO.model_validate(updated_institute)

    async def get_all(self) -> List[InstituteDTO]:
        institutes = await self.__institute_repository.get_all()

        return [InstituteDTO.model_validate(institute) for institute in institutes]

    async def get_by_id(self, institute_id: int) -> InstituteDTO:
        institute = await self.__institute_repository.get_by_id(institute_id=institute_id)

        if institute is None:
            raise InstituteNotFoundError(institute_id=institute_id)

        return InstituteDTO.model_validate(institute)

    async def get_by_name(self, institute_name: str) -> InstituteDTO:
        institute = await self.__institute_repository.get_by_name(institute_name=institute_name)

        if institute is None:
            raise InstituteNameNotFoundError(institute_name=institute_name)

        return InstituteDTO.model_validate(institute)

    async def delete_institute_by_id(self, institute_id: int) -> None:
        institute = await self.__institute_repository.get_by_id(institute_id=institute_id)

        if institute is None:
            raise InstituteNotFoundError(institute_id=institute_id)

        if not institute.deletable:
            raise InstituteCannotBeDeletedError(institute_id=institute_id)

        await self.__institute_repository.delete_institute_by_id(institute_model=institute)