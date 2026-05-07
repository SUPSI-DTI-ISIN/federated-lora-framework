import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from services.sse.sse_service import SseService


@pytest.fixture(autouse=True)
def reset_singleton():
    SseService._SseService__INSTANCE = None
    yield
    SseService._SseService__INSTANCE = None


@pytest.fixture()
def service():
    return SseService.get_instance(redis_client_async=MagicMock())


class TestGetInstance:
    def test_returns_same_object_on_repeated_calls(self):
        mock_redis = MagicMock()
        assert SseService.get_instance(redis_client_async=mock_redis) is SseService.get_instance(redis_client_async=mock_redis)

    def test_returns_non_none_instance(self):
        assert SseService.get_instance(redis_client_async=MagicMock()) is not None


class TestGenerateSseEvents:
    async def test_yields_event_when_message_received(self, service):
        from schemas.celery import CeleryJobDTO, CeleryJobResultType

        dto = CeleryJobDTO(job_id="t", result_type=CeleryJobResultType.SUCCESS)
        message = {"data": dto.model_dump_json()}

        mock_pubsub = AsyncMock()
        mock_pubsub.get_message = AsyncMock(side_effect=[message, None])
        mock_pubsub.subscribe = AsyncMock()
        mock_pubsub.unsubscribe = AsyncMock()
        mock_pubsub.close = AsyncMock()

        service._SseService__redis_client_async.pubsub = MagicMock(return_value=mock_pubsub)

        call_count = 0

        async def mock_is_disconnected():
            nonlocal call_count
            call_count += 1
            return call_count > 2

        mock_request = MagicMock()
        mock_request.is_disconnected = mock_is_disconnected

        with patch("asyncio.sleep", new_callable=AsyncMock):
            events = []
            async for event in service.generate_sse_events(request=mock_request):
                events.append(event)

        assert len(events) == 1

    async def test_unsubscribes_on_disconnect(self, service):
        mock_pubsub = AsyncMock()
        mock_pubsub.get_message = AsyncMock(return_value=None)
        mock_pubsub.subscribe = AsyncMock()
        mock_pubsub.unsubscribe = AsyncMock()
        mock_pubsub.close = AsyncMock()

        service._SseService__redis_client_async.pubsub = MagicMock(return_value=mock_pubsub)

        mock_request = MagicMock()
        mock_request.is_disconnected = AsyncMock(return_value=True)

        with patch("asyncio.sleep", new_callable=AsyncMock):
            async for _ in service.generate_sse_events(request=mock_request):
                pass

        mock_pubsub.unsubscribe.assert_awaited_once()
        mock_pubsub.close.assert_awaited_once()
