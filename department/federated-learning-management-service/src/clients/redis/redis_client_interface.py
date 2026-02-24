from abc import ABC, abstractmethod

import redis.asyncio
from redis import Redis


class RedisClientInterface(ABC):
    @abstractmethod
    def get_redis_client_sync(self) -> Redis:
        raise NotImplementedError

    @abstractmethod
    def get_redis_client_async(self) -> redis.asyncio.Redis:
        raise NotImplementedError