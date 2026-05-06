from unittest.mock import MagicMock

from services.inference.redis.dependencies import get_inference_result_redis_event_consumer
from services.inference.redis.inference_result_redis_event_consumer import InferenceResultRedisEventConsumer


class TestGetInferenceResultRedisEventConsumer:
    def test_returns_consumer_instance(self):
        mock_redis = MagicMock()
        consumer = get_inference_result_redis_event_consumer(redis_client_async=mock_redis)
        assert isinstance(consumer, InferenceResultRedisEventConsumer)
