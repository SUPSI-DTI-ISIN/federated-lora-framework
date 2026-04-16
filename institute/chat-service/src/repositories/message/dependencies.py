from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .message_repository_interface import MessageRepositoryInterface
from .message_repository import MessageRepository
from database import get_db_session

def get_message_repository(db: AsyncSession = Depends(get_db_session)) -> MessageRepositoryInterface:
    return MessageRepository(db_session=db)

def build_message_repository(db: AsyncSession) -> MessageRepositoryInterface:
    return MessageRepository(db_session=db)