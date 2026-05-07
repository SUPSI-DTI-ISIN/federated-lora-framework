from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from entities import MessageModel
from .message_repository_interface import MessageRepositoryInterface


class MessageRepository(MessageRepositoryInterface):
    def __init__(self, db_session: AsyncSession):
        self._db_session: AsyncSession = db_session

    async def get_all_by_chat(self, chat_id: int) -> List[MessageModel]:
        try:
            stmt = (
                select(MessageModel)
                .where(MessageModel.chat_id == chat_id)
                .order_by(MessageModel.created_at.desc())
            )
            result = await self._db_session.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as exc:
            raise exc

    async def get_all_by_chat_with_limit(self, chat_id: int, limit: int) -> List[MessageModel]:
        try:
            stmt = (
                select(MessageModel)
                .where(MessageModel.chat_id == chat_id)
                .order_by(MessageModel.created_at.desc())
                .limit(limit)
            )
            result = await self._db_session.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as exc:
            raise exc

    async def save_message(self, message_model: MessageModel) -> MessageModel:
        try:
            self._db_session.add(message_model)
            await self._db_session.commit()
            await self._db_session.refresh(message_model)
            return message_model
        except SQLAlchemyError as exc:
            await self._db_session.rollback()
            raise exc

    async def get_latest_by_chat(self, chat_id: int) -> Optional[MessageModel]:
        try:
            stmt = (
                select(MessageModel)
                .where(MessageModel.chat_id == chat_id)
                .order_by(MessageModel.created_at.desc())
                .limit(1)
            )
            result = await self._db_session.execute(stmt)
            return result.scalars().first()
        except SQLAlchemyError as exc:
            raise exc