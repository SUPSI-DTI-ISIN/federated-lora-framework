from unittest.mock import AsyncMock

from repositories.chat.dependencies import get_chat_repository, build_chat_repository
from repositories.chat.chat_repository import ChatRepository


class TestGetChatRepository:
    def test_returns_chat_repository_instance(self):
        mock_session = AsyncMock()
        repo = get_chat_repository(db=mock_session)
        assert isinstance(repo, ChatRepository)


class TestBuildChatRepository:
    def test_returns_chat_repository_instance(self):
        mock_session = AsyncMock()
        repo = build_chat_repository(db=mock_session)
        assert isinstance(repo, ChatRepository)
