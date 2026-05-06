import pytest
from abc import ABC

from services.redis.redis_event_consumer_service_interface import RedisEventConsumerServiceInterface


class TestRedisEventConsumerServiceInterface:
    def test_is_abstract(self):
        assert issubclass(RedisEventConsumerServiceInterface, ABC)

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            RedisEventConsumerServiceInterface()

    def test_abstract_methods_defined(self):
        assert RedisEventConsumerServiceInterface.__abstractmethods__ == {"start_redis_event_consumer"}

    def test_complete_subclass_can_be_instantiated(self):
        class Concrete(RedisEventConsumerServiceInterface):
            async def start_redis_event_consumer(self): ...

        assert isinstance(Concrete(), RedisEventConsumerServiceInterface)

    async def test_abstract_method_body_raises_not_implemented(self):
        class CallerThrough(RedisEventConsumerServiceInterface):
            async def start_redis_event_consumer(self):
                return await super().start_redis_event_consumer()

        with pytest.raises(NotImplementedError):
            await CallerThrough().start_redis_event_consumer()

    def test_redis_init_exports(self):
        from services.redis import RedisEventConsumerServiceInterface as I
        assert I is RedisEventConsumerServiceInterface

    def test_redis_init_version(self):
        import services.redis as sr
        assert sr.__version__ == "1.0.0"
