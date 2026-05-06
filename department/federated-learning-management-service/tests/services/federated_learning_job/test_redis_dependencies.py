import pytest
from unittest.mock import MagicMock, patch

from services.federated_learning_job.redis.federated_learning_job_redis_event_consumer import (
    FederatedLearningJobRedisEventConsumer,
)
from services.redis import RedisEventConsumerServiceInterface


@pytest.fixture(autouse=True)
def reset_singleton():
    FederatedLearningJobRedisEventConsumer._FederatedLearningJobRedisEventConsumer__INSTANCE = None
    yield
    FederatedLearningJobRedisEventConsumer._FederatedLearningJobRedisEventConsumer__INSTANCE = None


class TestGetFederatedLearningJobRedisEventConsumer:
    def test_returns_redis_event_consumer_interface(self):
        from services.federated_learning_job.redis.dependencies import (
            get_federated_learning_job_redis_event_consumer,
        )
        result = get_federated_learning_job_redis_event_consumer(redis_client_async=MagicMock())
        assert isinstance(result, RedisEventConsumerServiceInterface)

    def test_returns_singleton(self):
        from services.federated_learning_job.redis.dependencies import (
            get_federated_learning_job_redis_event_consumer,
        )
        mock_redis = MagicMock()
        a = get_federated_learning_job_redis_event_consumer(redis_client_async=mock_redis)
        b = get_federated_learning_job_redis_event_consumer(redis_client_async=mock_redis)
        assert a is b

    def test_redis_init_exports(self):
        from services.federated_learning_job.redis import get_federated_learning_job_redis_event_consumer as fn
        assert fn is not None

    def test_redis_init_version(self):
        import services.federated_learning_job.redis as r
        assert r.__version__ == "1.0.0"
