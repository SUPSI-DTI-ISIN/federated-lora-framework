from abc import ABC, abstractmethod
from typing import Optional

from models import SectionModel


class SectionsRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_id(self, section_id: int) -> Optional[SectionModel]:
        raise NotImplementedError

    @abstractmethod
    async def delete_section(self, section_model: SectionModel) -> None:
        raise NotImplementedError