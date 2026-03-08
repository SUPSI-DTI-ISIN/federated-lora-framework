from abc import ABC, abstractmethod
from typing import List

from schemas.institute import InstituteDTO, InstituteCreationRequestDTO, InstituteUpdateRequestDTO


class InstituteServiceInterface(ABC):
    @abstractmethod
    async def create_new_institute(self, institute_creation_request_dto: InstituteCreationRequestDTO) -> InstituteDTO:
        raise NotImplementedError

    @abstractmethod
    async def update_institute(self, institute_id: int, institute_update_request_dto: InstituteUpdateRequestDTO) -> InstituteDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[InstituteDTO]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, institute_id: int) -> InstituteDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, institute_name: str) -> InstituteDTO:
        raise NotImplementedError

    @abstractmethod
    async def delete_institute_by_id(self, institute_id: int) -> None:
        raise NotImplementedError