from abc import ABC, abstractmethod

class RedisEventConsumerServiceInterface(ABC):
    @abstractmethod
    async def start_redis_event_consumer(self):
        raise NotImplementedError