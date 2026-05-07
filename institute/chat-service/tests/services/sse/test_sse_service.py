import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch, AsyncMock

from entities import MessageModel, MessageRole
from schemas.celery import CeleryJobResultType, CeleryJobDTO, QueryResponseDTO
from services.sse.sse_service import SseService


def _assistant_message(chat_id=10):
    m = MessageModel()
    m.id = 99
    m.chat_id = chat_id
    m.role = MessageRole.ASSISTANT
    m.content = "Hi there"
    m.model_key = "model-v1"
    m.adapter_version = 1
    m.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return m


def _user_message(chat_id=10):
    m = MessageModel()
    m.id = 98
    m.chat_id = chat_id
    m.role = MessageRole.USER
    m.content = "Hello"
    m.model_key = "model-v1"
    m.adapter_version = 1
    m.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return m


@pytest.fixture(autouse=True)
def reset_singleton():
    SseService._SseService__INSTANCE = None
    yield
    SseService._SseService__INSTANCE = None


@pytest.fixture()
def redis_client():
    return MagicMock()


@pytest.fixture()
def message_repo():
    return AsyncMock()


@pytest.fixture()
def service(redis_client, message_repo):
    return SseService(
        redis_client_async=redis_client,
        message_repository=message_repo,
        poll_max_attempts=3,
        poll_interval=0,
    )


class TestPollAssistantMessage:
    async def test_returns_message_dto_when_assistant_message_found(self, service, message_repo):
        msg = _assistant_message()
        message_repo.get_latest_by_chat = AsyncMock(return_value=msg)

        result = await service._SseService__poll_assistant_message(chat_id=10)

        assert result is not None
        assert result.role == MessageRole.ASSISTANT.value

    async def test_returns_none_when_no_assistant_message_after_max_attempts(self, service, message_repo):
        message_repo.get_latest_by_chat = AsyncMock(return_value=_user_message())

        result = await service._SseService__poll_assistant_message(chat_id=10)

        assert result is None
        assert message_repo.get_latest_by_chat.await_count == 3

    async def test_returns_none_when_no_message_at_all(self, service, message_repo):
        message_repo.get_latest_by_chat = AsyncMock(return_value=None)

        result = await service._SseService__poll_assistant_message(chat_id=10)

        assert result is None

    async def test_returns_on_first_successful_attempt(self, service, message_repo):
        msg = _assistant_message()
        message_repo.get_latest_by_chat = AsyncMock(return_value=msg)

        result = await service._SseService__poll_assistant_message(chat_id=10)

        assert result is not None
        message_repo.get_latest_by_chat.assert_awaited_once()


class TestGetInstance:
    def test_returns_same_instance(self, redis_client, message_repo):
        instance1 = SseService.get_instance(redis_client_async=redis_client, message_repository=message_repo)
        instance2 = SseService.get_instance(redis_client_async=redis_client, message_repository=message_repo)
        assert instance1 is instance2

    def test_creates_new_instance_after_reset(self, redis_client, message_repo):
        instance1 = SseService.get_instance(redis_client_async=redis_client, message_repository=message_repo)
        SseService._SseService__INSTANCE = None
        instance2 = SseService.get_instance(redis_client_async=redis_client, message_repository=message_repo)
        assert instance1 is not instance2
