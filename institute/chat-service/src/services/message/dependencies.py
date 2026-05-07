from typing import Optional

from fastapi import Depends

from .message_service import MessageService
from .message_service_interface import MessageServiceInterface
from repositories.message import get_message_repository, MessageRepositoryInterface
from config import settings

def get_message_service(message_repository: MessageRepositoryInterface = Depends(get_message_repository), conversation_history_limit: Optional[int] = settings.conversation_history_limit) -> MessageServiceInterface:
    return MessageService(message_repository=message_repository, conversation_history_limit=conversation_history_limit)