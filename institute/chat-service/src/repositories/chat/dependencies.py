from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .chat_repository_interface import ChatRepositoryInterface
from .chat_repository import ChatRepository
from database import get_db_session

def get_chat_repository(db: AsyncSession = Depends(get_db_session)) -> ChatRepositoryInterface:
    return ChatRepository(db_session=db)


def build_chat_repository(db: AsyncSession) -> ChatRepositoryInterface:
    return ChatRepository(db_session=db)