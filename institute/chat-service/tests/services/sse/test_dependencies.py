from unittest.mock import AsyncMock, MagicMock

from services.sse.dependencies import get_sse_service, get_custom_ping
from services.sse.sse_service import SseService


class TestGetSseService:
    def test_returns_sse_service_instance(self):
        mock_redis = MagicMock()
        mock_repo = AsyncMock()
        service = get_sse_service(redis_client_async=mock_redis, message_repository=mock_repo)
        assert isinstance(service, SseService)


class TestGetCustomPing:
    def test_returns_server_sent_event(self):
        ping = get_custom_ping()
        assert ping is not None
