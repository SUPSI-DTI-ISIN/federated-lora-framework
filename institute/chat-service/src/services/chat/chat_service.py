from typing import List

from datetime import datetime, timezone

from entities import ChatModel
from repositories.chat import ChatRepositoryInterface
from schemas.chat import ChatDTO, ChatCreationRequestDTO
from schemas.exceptions import ChatNotFoundError
from .chat_service_interface import ChatServiceInterface


class ChatService(ChatServiceInterface):
    def __init__(self, chat_repository: ChatRepositoryInterface):
        self.__chat_repository = chat_repository

    async def create_new_chat(self, chat_creation_request_dto: ChatCreationRequestDTO, user_id: str) -> ChatDTO:
        new_chat = ChatModel(
            user_id=user_id,
            title=chat_creation_request_dto.title,
            messages=[],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        new_chat_created = await self.__chat_repository.save_chat(chat_model=new_chat)
        return ChatDTO.model_validate(new_chat_created)

    async def update_chat_modification_date(self, chat_id: int) -> ChatDTO:
        chat = await self.__chat_repository.get_by_id(chat_id=chat_id)

        if chat is None:
            raise ChatNotFoundError(chat_id=chat_id)

        chat.updated_at = datetime.now(timezone.utc)

        chat_updated = await self.__chat_repository.save_chat(chat_model=chat)

        return ChatDTO.model_validate(chat_updated)

    async def update_chat_inference_state(self, chat_id: int, is_doing_inference: bool) -> ChatDTO:
        chat = await self.__chat_repository.get_by_id(chat_id=chat_id)

        if chat is None:
            raise ChatNotFoundError(chat_id=chat_id)

        chat.is_doing_inference = is_doing_inference

        chat_updated = await self.__chat_repository.save_chat(chat_model=chat)

        return ChatDTO.model_validate(chat_updated)

    async def get_all_by_user(self, user_id: str) -> List[ChatDTO]:
        user_chats = await self.__chat_repository.get_all_by_user(user_id=user_id)

        return [ChatDTO.model_validate(chat) for chat in user_chats]

    async def get_by_id(self, chat_id: int) -> ChatDTO:
        chat = await self.__chat_repository.get_by_id(chat_id=chat_id)

        if chat is None:
            raise ChatNotFoundError(chat_id=chat_id)

        return ChatDTO.model_validate(chat)

    async def delete_chat_by_user(self, chat_id: int) -> None:
        chat = await self.__chat_repository.get_by_id(chat_id=chat_id)

        if chat is None:
            raise ChatNotFoundError(chat_id=chat_id)

        await self.__chat_repository.delete_chat_by_user(chat_model=chat)