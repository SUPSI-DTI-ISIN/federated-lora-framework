from abc import ABC, abstractmethod
from typing import List

from schemas.documents import DocumentDTO


class SectionsServiceInterface(ABC):
    @abstractmethod
    async def delete_by_id(self, section_id: int) -> None:
        raise NotImplementedError