from typing import List

from entities import ChatModel
from repositories.chat import ChatRepositoryInterface
from schemas.chat import ChatDTO
from schemas.chat.chat_creation_request_dto import ChatCreationRequestDTO
from schemas.exceptions import ChatNotFoundError
from .chat_service_interface import ChatServiceInterface


class ChatService(ChatServiceInterface):
    def __init__(self, chat_repository: ChatRepositoryInterface):
        self.__chat_repository = chat_repository

    async def create_new_chat(self, chat_creation_request_dto: ChatCreationRequestDTO, user_id: str) -> ChatDTO:
        new_chat = ChatModel(
            user_id=user_id,
            title=chat_creation_request_dto.title,
            messages=[]
        )

        new_chat_created = await self.__chat_repository.save_chat(chat_model=new_chat)
        return ChatDTO.model_validate(new_chat_created)


    async def get_all_by_user(self, user_id: str) -> List[ChatDTO]:
        user_chats = await self.__chat_repository.get_all_by_user(user_id=user_id)

        return [ChatDTO.model_validate(chat) for chat in user_chats]

    async def get_by_id(self, chat_id: int) -> ChatDTO:
        user_chat = await self.__chat_repository.get_by_id(chat_id=chat_id)

        if user_chat is None:
            raise ChatNotFoundError(chat_id=chat_id)

        return ChatDTO.model_validate(user_chat)

    async def delete_chat_by_user(self, chat_id: int) -> None:
        user_chat = await self.__chat_repository.get_by_id(chat_id=chat_id)

        if user_chat is None:
            raise ChatNotFoundError(chat_id=chat_id)

        await self.__chat_repository.delete_chat_by_user(chat_model=user_chat)