from clients.redis.dependencies import get_redis_client, get_redis_client_sync, build_redis_client_async, get_redis_client_async
from clients.redis.redis_client_service import RedisClientService


class TestGetRedisClient:
    def test_returns_redis_client_service_instance(self):
        client = get_redis_client()
        assert isinstance(client, RedisClientService)


class TestGetRedisClientSync:
    def test_returns_sync_redis_client(self):
        client = get_redis_client_sync()
        assert client is not None


class TestBuildRedisClientAsync:
    def test_returns_async_redis_client(self):
        client = build_redis_client_async()
        assert client is not None


class TestGetRedisClientAsync:
    def test_returns_async_redis_client(self):
        # get_redis_client_async uses FastAPI Depends, so inject the service directly
        svc = get_redis_client()
        client = get_redis_client_async(redis_client_service=svc)
        assert client is not None
