from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database import DatabaseConnector
from repositories.chat import ChatRepository, ChatRepositoryInterface
from services.chat import ChatService, ChatServiceInterface


def get_chat_repository(db: AsyncSession = Depends(DatabaseConnector.get_db_session)) -> ChatRepositoryInterface:
    return ChatRepository(db_session=db)

def get_chat_service(chat_repository: ChatRepositoryInterface = Depends(get_chat_repository)) -> ChatServiceInterface:
    return ChatService(chat_repository=chat_repository)