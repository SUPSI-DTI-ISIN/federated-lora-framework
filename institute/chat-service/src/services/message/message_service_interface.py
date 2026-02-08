from abc import ABC, abstractmethod
from typing import List

from schemas.message import MessageDTO, InferenceRequestDTO


class MessageServiceInterface(ABC):
    @abstractmethod
    async def create_new_message(self, message_dto: MessageDTO) -> MessageDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_chat(self, chat_id: int) -> List[MessageDTO]:
        raise NotImplementedError