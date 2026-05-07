from abc import ABC, abstractmethod
from typing import List, Optional

from entities import ChatModel


class ChatRepositoryInterface(ABC):
    @abstractmethod
    async def save_chat(self, chat_model: ChatModel) -> ChatModel:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_user(self, user_id: str) -> List[ChatModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, chat_id: int) -> Optional[ChatModel]:
        raise NotImplementedError

    @abstractmethod
    async def delete_chat_by_user(self, chat_model: ChatModel) -> None:
        raise NotImplementedError