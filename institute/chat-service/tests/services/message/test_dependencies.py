from unittest.mock import AsyncMock

from services.message.dependencies import get_message_service
from services.message.message_service import MessageService


class TestGetMessageService:
    def test_returns_message_service_instance(self):
        mock_repo = AsyncMock()
        service = get_message_service(message_repository=mock_repo)
        assert isinstance(service, MessageService)
