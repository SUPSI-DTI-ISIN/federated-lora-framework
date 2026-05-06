import pytest
from unittest.mock import MagicMock, patch

from clients.redis.redis_client_service import RedisClientService


@pytest.fixture(autouse=True)
def reset_singleton():
    RedisClientService._RedisClientService__INSTANCE = None
    yield
    RedisClientService._RedisClientService__INSTANCE = None


class TestGetInstance:
    def test_returns_same_object_on_repeated_calls(self):
        a = RedisClientService.get_instance(redis_url="redis://localhost:6379")
        b = RedisClientService.get_instance(redis_url="redis://localhost:6379")
        assert a is b

    def test_returns_non_none_instance(self):
        assert RedisClientService.get_instance(redis_url="redis://localhost:6379") is not None


class TestProperties:
    def test_redis_client_sync_returns_sync_client(self):
        svc = RedisClientService.get_instance(redis_url="redis://localhost:6379")
        assert svc.redis_client_sync is not None

    def test_redis_client_async_returns_async_client(self):
        svc = RedisClientService.get_instance(redis_url="redis://localhost:6379")
        assert svc.redis_client_async is not None


class TestRedisClientInit:
    def test_redis_init_exports(self):
        from clients.redis import get_redis_client_sync, get_redis_client_async, build_redis_client_async
        assert get_redis_client_sync is not None
        assert get_redis_client_async is not None
        assert build_redis_client_async is not None

    def test_redis_init_version(self):
        import clients.redis as cr
        assert cr.__version__ == "1.0.0"


class TestRedisDependencies:
    def test_get_redis_client_sync_returns_sync_client(self):
        from clients.redis.dependencies import get_redis_client_sync
        result = get_redis_client_sync()
        assert result is not None

    def test_build_redis_client_async_returns_async_client(self):
        from clients.redis.dependencies import build_redis_client_async
        result = build_redis_client_async()
        assert result is not None

    def test_get_redis_client_async_returns_async_client(self):
        from clients.redis.dependencies import get_redis_client_async, get_redis_client
        svc = get_redis_client()
        result = get_redis_client_async(redis_client_service=svc)
        assert result is not None
