from abc import ABC, abstractmethod


class DocumentsRepositoryInterface(ABC):
    @abstractmethod
    async def get_all(self) -> None:
        raise NotImplementedError