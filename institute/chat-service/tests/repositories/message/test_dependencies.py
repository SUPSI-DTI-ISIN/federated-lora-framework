from unittest.mock import AsyncMock

from repositories.message.dependencies import get_message_repository, build_message_repository
from repositories.message.message_repository import MessageRepository


class TestGetMessageRepository:
    def test_returns_message_repository_instance(self):
        mock_session = AsyncMock()
        repo = get_message_repository(db=mock_session)
        assert isinstance(repo, MessageRepository)


class TestBuildMessageRepository:
    def test_returns_message_repository_instance(self):
        mock_session = AsyncMock()
        repo = build_message_repository(db=mock_session)
        assert isinstance(repo, MessageRepository)
