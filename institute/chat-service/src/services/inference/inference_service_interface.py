from abc import ABC, abstractmethod
from typing import List

from clients.schemas import QueryResponseDTO
from schemas.chat import ConversationDTO
from schemas.message import MessageDTO


class InferenceServiceInterface(ABC):
    @abstractmethod
    async def inference_model(self, user_id: str, chat_id: int, user_message: MessageDTO, conversation_history: List[ConversationDTO]) -> bool:
        raise NotImplementedError