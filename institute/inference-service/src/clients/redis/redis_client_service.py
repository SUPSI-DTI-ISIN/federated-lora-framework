import redis

from redis import Redis

class RedisClientService:
    __INSTANCE = None

    def __init__(self, redis_url: str):
        self.__redis_client_sync = redis.from_url(url=redis_url, decode_responses=True)
        self.__redis_client_async = redis.asyncio.from_url(url=redis_url, decode_responses=True)

    @classmethod
    def get_instance(cls, redis_url: str):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(redis_url=redis_url)
        return cls.__INSTANCE

    @property
    def redis_client_sync(self) -> Redis:
        return self.__redis_client_sync

    @property
    def redis_client_async(self) -> redis.asyncio.Redis:
        return self.__redis_client_async