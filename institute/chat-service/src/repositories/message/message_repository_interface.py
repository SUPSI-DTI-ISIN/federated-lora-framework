from abc import ABC, abstractmethod
from typing import List, Optional

from entities import MessageModel


class MessageRepositoryInterface(ABC):
    @abstractmethod
    async def get_all_by_chat(self, chat_id: int) -> List[MessageModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_chat_with_limit(self, chat_id: int, limit: int) -> List[MessageModel]:
        raise NotImplementedError

    @abstractmethod
    async def save_message(self, message_model: MessageModel) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_latest_by_chat(self, chat_id: int) -> Optional[MessageModel]:
        raise NotImplementedError