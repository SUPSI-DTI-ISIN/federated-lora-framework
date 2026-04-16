import redis

from redis import Redis
from fastapi import Depends

from config import settings
from .redis_client_service import RedisClientService

def get_redis_client(redis_url: str = settings.redis_url) -> RedisClientService:
    return RedisClientService.get_instance(redis_url=redis_url)

def get_redis_client_sync(redis_client_service: RedisClientService = get_redis_client()) -> Redis:
    return redis_client_service.redis_client_sync

def build_redis_client_async(redis_client_service: RedisClientService = get_redis_client()) -> redis.asyncio.Redis:
    return redis_client_service.redis_client_async

def get_redis_client_async(redis_client_service: RedisClientService = Depends(get_redis_client)) -> redis.asyncio.Redis:
    return redis_client_service.redis_client_async