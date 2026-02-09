from typing import List, Optional
from datetime import datetime, timezone

from entities import MessageModel
from repositories.message.message_repository_interface import MessageRepositoryInterface
from schemas.message import MessageDTO, MessageCreationRequestDTO
from .message_service_interface import MessageServiceInterface

class MessageService(MessageServiceInterface):
    def __init__(self, message_repository: MessageRepositoryInterface, conversation_history_limit: Optional[int]):
        self.__message_repository = message_repository
        self.__conversation_history_limit = conversation_history_limit

    async def create_new_message(self, message_creation_request_dto: MessageCreationRequestDTO) -> MessageDTO:
        message = MessageModel(
            chat_id=message_creation_request_dto.chat_id,
            role=message_creation_request_dto.role,
            content=message_creation_request_dto.content,
            model_key=message_creation_request_dto.model_key,
            adapter_version=message_creation_request_dto.adapter_version,
            created_at=datetime.now(timezone.utc)
        )

        created_message = await self.__message_repository.save_message(message_model=message)

        return MessageDTO.model_validate(created_message)

    async def get_all_by_chat(self, chat_id: int) -> List[MessageDTO]:
        chat_messages = await self.__message_repository.get_all_by_chat(chat_id=chat_id) if self.__conversation_history_limit is None else await self.__message_repository.get_all_by_chat_with_limit(chat_id=chat_id, limit=self.__conversation_history_limit)

        return [MessageDTO.model_validate(message) for message in chat_messages]