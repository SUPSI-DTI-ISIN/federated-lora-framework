import pytest
from unittest.mock import MagicMock

from clients.redis.redis_client_service import RedisClientService
from clients.redis.dependencies import (
    get_redis_client,
    get_redis_client_sync,
    build_redis_client_async,
    get_redis_client_async,
)


@pytest.fixture(autouse=True)
def reset_singleton():
    RedisClientService._RedisClientService__INSTANCE = None
    yield
    RedisClientService._RedisClientService__INSTANCE = None


class TestGetRedisClient:
    def test_returns_redis_client_service(self):
        svc = get_redis_client()
        assert isinstance(svc, RedisClientService)


class TestGetRedisClientSync:
    def test_returns_sync_client(self):
        client = get_redis_client_sync()
        assert client is not None


class TestBuildRedisClientAsync:
    def test_returns_async_client(self):
        client = build_redis_client_async()
        assert client is not None


class TestGetRedisClientAsync:
    def test_returns_async_client_with_injected_service(self):
        svc = get_redis_client()
        client = get_redis_client_async(redis_client_service=svc)
        assert client is not None
