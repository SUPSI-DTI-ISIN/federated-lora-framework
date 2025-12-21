from abc import ABC, abstractmethod


class DocumentsServiceInterface(ABC):
    @abstractmethod
    async def upload_data(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> None:
        raise NotImplementedError