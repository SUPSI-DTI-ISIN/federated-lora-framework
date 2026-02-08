from typing import List

from repositories.message.message_repository_interface import MessageRepositoryInterface
from schemas.message import MessageDTO
from .message_service_interface import MessageServiceInterface

class MessageService(MessageServiceInterface):
    def __init__(self, message_repository: MessageRepositoryInterface):
        self.__message_repository = message_repository

    async def create_new_message(self, message_dto: MessageDTO) -> MessageDTO:
        raise NotImplementedError

    async def get_all_by_chat(self, chat_id: int) -> List[MessageDTO]:
        chat_messages = await self.__message_repository.get_all_by_chat(chat_id=chat_id)

        return [MessageDTO.model_validate(message) for message in chat_messages]