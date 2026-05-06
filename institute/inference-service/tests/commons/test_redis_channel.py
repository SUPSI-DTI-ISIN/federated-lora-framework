from enum import Enum
from commons.redis_channel import RedisChannel


class TestRedisChannel:
    def test_is_enum(self):
        assert issubclass(RedisChannel, Enum)

    def test_inference_result_value(self):
        assert RedisChannel.INFERENCE_RESULT.value == "inference:result"

    def test_all_members(self):
        assert set(RedisChannel.__members__) == {"INFERENCE_RESULT"}


class TestCommonsInit:
    def test_redis_channel_exported(self):
        from commons import RedisChannel as RC
        assert RC is RedisChannel

    def test_version(self):
        import commons
        assert commons.__version__ == "1.0.0"

    def test_all_list(self):
        import commons
        assert "RedisChannel" in commons.__all__
