from config import settings
from clients.redis.client.redis_client_interface import RedisClientInterface
from clients.redis.client.redis_client import RedisClient

redis: RedisClientInterface = RedisClient.get_instance(redis_url=settings.redis_url)
redis_client_sync = redis.get_redis_client_sync()
redis_client_async = redis.get_redis_client_async()

__all__ = [
    'redis_client_sync',
    'redis_client_async'
]

__version__ = "1.0.0"