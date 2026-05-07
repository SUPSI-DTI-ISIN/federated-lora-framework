from fastapi import Depends

from .chat_service import ChatService
from .chat_service_interface import ChatServiceInterface
from repositories.chat import get_chat_repository, ChatRepositoryInterface

def get_chat_service(chat_repository: ChatRepositoryInterface = Depends(get_chat_repository)) -> ChatServiceInterface:
    return ChatService(chat_repository=chat_repository)