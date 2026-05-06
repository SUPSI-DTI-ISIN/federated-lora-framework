from unittest.mock import AsyncMock

from services.chat.dependencies import get_chat_service
from services.chat.chat_service import ChatService


class TestGetChatService:
    def test_returns_chat_service_instance(self):
        mock_repo = AsyncMock()
        service = get_chat_service(chat_repository=mock_repo)
        assert isinstance(service, ChatService)
