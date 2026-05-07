from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from entities import ChatModel
from .chat_repository_interface import ChatRepositoryInterface


class ChatRepository(ChatRepositoryInterface):
    def __init__(self, db_session: AsyncSession):
        self._db_session: AsyncSession = db_session

    async def save_chat(self, chat_model: ChatModel) -> ChatModel:
        try:
            self._db_session.add(chat_model)
            await self._db_session.commit()
            await self._db_session.refresh(chat_model)
            return chat_model
        except SQLAlchemyError as exc:
            await self._db_session.rollback()
            raise exc

    async def get_all_by_user(self, user_id: str) -> List[ChatModel]:
        try:
            stmt = (
                select(ChatModel)
                .where(ChatModel.user_id == user_id)
                .order_by(ChatModel.updated_at.desc())
            )
            result = await self._db_session.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as exc:
            raise exc

    async def get_by_id(self, chat_id: int) -> Optional[ChatModel]:
        try:
            model = await self._db_session.get(ChatModel, chat_id)
            return model
        except SQLAlchemyError as exc:
            raise exc

    async def delete_chat_by_user(self, chat_model: ChatModel) -> None:
        try:
            await self._db_session.delete(chat_model)
            await self._db_session.commit()
        except SQLAlchemyError as exc:
            await self._db_session.rollback()
            raise exc