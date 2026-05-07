from abc import ABC, abstractmethod
from typing import List

from schemas.documents import DocumentDTO, UpdateSectionRequestDTO, SectionDTO


class SectionsServiceInterface(ABC):
    @abstractmethod
    async def delete_by_id(self, section_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_section_content(self, section_id: int, update_section_content_request_dto: UpdateSectionRequestDTO) -> SectionDTO:
        raise NotImplementedError