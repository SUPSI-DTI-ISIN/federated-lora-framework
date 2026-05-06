import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from entities import MessageModel, MessageRole
from datetime import datetime, timezone
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


def _success_celery_dto(chat_id=10):
    return CeleryJobDTO(
        job_id="job-1",
        result_type=CeleryJobResultType.SUCCESS,
        chat_id=chat_id,
        result=QueryResponseDTO(
            user_id="u-1",
            chat_id=chat_id,
            prompt="Hello",
            response="Hi",
            model_key="model-v1",
            adapter_version=1,
        ),
    )


def _failure_celery_dto(chat_id=10):
    return CeleryJobDTO(
        job_id="job-2",
        result_type=CeleryJobResultType.FAILURE,
        chat_id=chat_id,
        error="Something went wrong",
    )


@pytest.fixture(autouse=True)
def reset_singleton():
    SseService._SseService__INSTANCE = None
    yield
    SseService._SseService__INSTANCE = None


@pytest.fixture()
def message_repo():
    return AsyncMock()


@pytest.fixture()
def redis_client():
    return MagicMock()


@pytest.fixture()
def service(redis_client, message_repo):
    return SseService(
        redis_client_async=redis_client,
        message_repository=message_repo,
        poll_max_attempts=2,
        poll_interval=0,
    )


async def _collect_events(service, redis_client, messages, message_repo_side_effect=None):
    """Helper to run generate_sse_events and collect yielded events."""
    mock_pubsub = AsyncMock()
    mock_pubsub.subscribe = AsyncMock()
    mock_pubsub.unsubscribe = AsyncMock()
    mock_pubsub.close = AsyncMock()

    msg_iter = iter(messages)

    async def _get_message(**kwargs):
        try:
            return next(msg_iter)
        except StopIteration:
            return None

    mock_pubsub.get_message = _get_message
    redis_client.pubsub = MagicMock(return_value=mock_pubsub)

    if message_repo_side_effect is not None:
        service._SseService__message_repository.get_latest_by_chat = AsyncMock(
            side_effect=message_repo_side_effect
        )

    request = MagicMock()
    # Disconnect after first iteration to stop the loop
    call_count = [0]

    async def _is_disconnected():
        call_count[0] += 1
        return call_count[0] > len(messages) + 1

    request.is_disconnected = _is_disconnected

    events = []
    async for event in service.generate_sse_events(request=request, user_id="u-1"):
        events.append(event)

    return events, mock_pubsub


class TestGenerateSseEvents:
    async def test_subscribes_and_unsubscribes(self, service, redis_client, message_repo):
        events, pubsub = await _collect_events(service, redis_client, [])
        pubsub.subscribe.assert_awaited_once()
        pubsub.unsubscribe.assert_awaited_once()
        pubsub.close.assert_awaited_once()

    async def test_disconnects_when_request_disconnected(self, service, redis_client, message_repo):
        events, pubsub = await _collect_events(service, redis_client, [])
        # No events since no messages were published
        assert events == []

    async def test_yields_failure_event_on_failure_dto(self, service, redis_client, message_repo):
        dto = _failure_celery_dto()
        messages = [{"data": dto.model_dump_json()}]

        events, _ = await _collect_events(service, redis_client, messages)

        assert len(events) == 1
        # The event data contains the failure DTO
        assert "failure" in events[0].data

    async def test_yields_success_event_when_assistant_message_found(self, service, redis_client, message_repo):
        dto = _success_celery_dto(chat_id=10)
        messages = [{"data": dto.model_dump_json()}]
        assistant_msg = _assistant_message(chat_id=10)

        events, _ = await _collect_events(
            service, redis_client, messages,
            message_repo_side_effect=[assistant_msg]
        )

        assert len(events) == 1
        assert "success" in events[0].event

    async def test_yields_failure_event_when_poll_returns_no_assistant_message(self, service, redis_client, message_repo):
        dto = _success_celery_dto(chat_id=10)
        messages = [{"data": dto.model_dump_json()}]

        # Poll always returns None
        events, _ = await _collect_events(
            service, redis_client, messages,
            message_repo_side_effect=[None, None]
        )

        assert len(events) == 1
        assert "failure" in events[0].event

    async def test_skips_none_messages(self, service, redis_client, message_repo):
        # None message should be skipped without yielding
        events, _ = await _collect_events(service, redis_client, [None])
        assert events == []
