import pytest
from unittest.mock import MagicMock

from services.sse.sse_service import SseService
from services.sse.dependencies import get_sse_service, get_custom_ping
from services.sse.sse_service_interface import SseServiceInterface


@pytest.fixture(autouse=True)
def reset_singleton():
    SseService._SseService__INSTANCE = None
    yield
    SseService._SseService__INSTANCE = None


class TestGetSseService:
    def test_returns_sse_service_interface(self):
        assert isinstance(get_sse_service(redis_client_async=MagicMock()), SseServiceInterface)

    def test_returns_singleton(self):
        mock_redis = MagicMock()
        assert get_sse_service(redis_client_async=mock_redis) is get_sse_service(redis_client_async=mock_redis)

    def test_sse_init_exports(self):
        from services.sse import SseServiceInterface, get_sse_service as fn, get_custom_ping as ping
        assert SseServiceInterface is not None
        assert fn is not None
        assert ping is not None

    def test_sse_init_version(self):
        import services.sse as ss
        assert ss.__version__ == "1.0.0"


class TestGetCustomPing:
    def test_returns_server_sent_event(self):
        from sse_starlette import ServerSentEvent
        result = get_custom_ping()
        assert isinstance(result, ServerSentEvent)
