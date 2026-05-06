import pytest
from unittest.mock import MagicMock, patch

from clients.redis.redis_client_service import RedisClientService


@pytest.fixture(autouse=True)
def reset_singleton():
    RedisClientService._RedisClientService__INSTANCE = None
    yield
    RedisClientService._RedisClientService__INSTANCE = None


class TestGetInstance:
    def test_returns_same_instance(self):
        i1 = RedisClientService.get_instance(redis_url="redis://localhost:6379")
        i2 = RedisClientService.get_instance(redis_url="redis://localhost:6379")
        assert i1 is i2

    def test_creates_new_instance_after_reset(self):
        i1 = RedisClientService.get_instance(redis_url="redis://localhost:6379")
        RedisClientService._RedisClientService__INSTANCE = None
        i2 = RedisClientService.get_instance(redis_url="redis://localhost:6379")
        assert i1 is not i2


class TestProperties:
    def test_redis_client_sync_property(self):
        svc = RedisClientService.get_instance(redis_url="redis://localhost:6379")
        assert svc.redis_client_sync is not None

    def test_redis_client_async_property(self):
        svc = RedisClientService.get_instance(redis_url="redis://localhost:6379")
        assert svc.redis_client_async is not None
