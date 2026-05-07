from repositories.sections import SectionsRepositoryInterface
from schemas.documents import UpdateSectionRequestDTO, SectionDTO
from schemas.exceptions import SectionNotFoundError
from .sections_service_interface import SectionsServiceInterface


class SectionsService(SectionsServiceInterface):
    def __init__(self, sections_repository: SectionsRepositoryInterface):
        self.__sections_repository = sections_repository

    async def delete_by_id(self, section_id: int) -> None:
        section_model = await self.__sections_repository.get_by_id(section_id=section_id)
        if section_model is None:
            raise SectionNotFoundError(section_id=section_id)

        await self.__sections_repository.delete_section(section_model=section_model)

    async def update_section_content(self, section_id: int, update_section_content_request_dto: UpdateSectionRequestDTO) -> SectionDTO:
        section_model = await self.__sections_repository.get_by_id(section_id=section_id)

        if section_model is None:
            raise SectionNotFoundError(section_id=section_id)

        section_model.content = update_section_content_request_dto.updated_content

        updated_section = await self.__sections_repository.save_section(section_model=section_model)

        return SectionDTO.model_validate(updated_section)