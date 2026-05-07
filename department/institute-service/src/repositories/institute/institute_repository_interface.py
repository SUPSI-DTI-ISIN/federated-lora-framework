from abc import ABC, abstractmethod
from typing import List, Optional

from entities import InstituteModel


class InstituteRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, institute_model: InstituteModel) -> InstituteModel:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[InstituteModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, institute_id: int) -> Optional[InstituteModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, institute_name: str) -> Optional[InstituteModel]:
        raise NotImplementedError

    @abstractmethod
    async def delete_institute_by_id(self, institute_model: InstituteModel) -> None:
        raise NotImplementedError