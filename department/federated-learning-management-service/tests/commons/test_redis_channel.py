from enum import Enum

from commons.redis_channel import RedisChannel


class TestRedisChannel:
    def test_is_enum(self):
        assert issubclass(RedisChannel, Enum)

    def test_job_updates_value(self):
        assert RedisChannel.JOB_UPDATES.value == "job_updates"

    def test_all_members(self):
        assert set(RedisChannel.__members__) == {"JOB_UPDATES"}


class TestCommonsInit:
    def test_redis_channel_is_exported(self):
        from commons import RedisChannel as RC
        assert RC is RedisChannel

    def test_version(self):
        import commons
        assert commons.__version__ == "1.0.0"

    def test_all_list(self):
        import commons
        assert "RedisChannel" in commons.__all__
