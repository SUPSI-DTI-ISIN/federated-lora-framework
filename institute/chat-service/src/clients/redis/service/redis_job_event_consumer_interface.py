from abc import ABC, abstractmethod


class RedisJobEventConsumerInterface(ABC):
    @abstractmethod
    async def start(self):
        raise NotImplementedError