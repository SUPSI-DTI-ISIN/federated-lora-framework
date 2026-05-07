from abc import ABC, abstractmethod
from typing import List

from schemas.chat import ChatDTO
from schemas.chat.chat_creation_request_dto import ChatCreationRequestDTO


class ChatServiceInterface(ABC):
    @abstractmethod
    async def create_new_chat(self, chat_creation_request_dto: ChatCreationRequestDTO, user_id: str) -> ChatDTO:
        raise NotImplementedError

    @abstractmethod
    async def update_chat_modification_date(self, chat_id: int) -> ChatDTO:
        raise NotImplementedError

    @abstractmethod
    async def update_chat_inference_state(self, chat_id: int, is_doing_inference: bool) -> ChatDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_user(self, user_id: str) -> List[ChatDTO]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, chat_id: int) -> ChatDTO:
        raise NotImplementedError

    @abstractmethod
    async def delete_chat_by_user(self, chat_id: int) -> None:
        raise NotImplementedError