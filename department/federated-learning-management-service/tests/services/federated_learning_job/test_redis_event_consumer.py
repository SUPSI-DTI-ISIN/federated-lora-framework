import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from entities import FederatedLearningJobStatus
from schemas.celery import CeleryJobDTO, CeleryJobResultType
from services.federated_learning_job.redis.federated_learning_job_redis_event_consumer import (
    FederatedLearningJobRedisEventConsumer,
)


@pytest.fixture(autouse=True)
def reset_singleton():
    FederatedLearningJobRedisEventConsumer._FederatedLearningJobRedisEventConsumer__INSTANCE = None
    yield
    FederatedLearningJobRedisEventConsumer._FederatedLearningJobRedisEventConsumer__INSTANCE = None


@pytest.fixture()
def consumer():
    return FederatedLearningJobRedisEventConsumer.get_instance(redis_client_async=MagicMock())


class TestGetInstance:
    def test_returns_same_object_on_repeated_calls(self):
        mock_redis = MagicMock()
        a = FederatedLearningJobRedisEventConsumer.get_instance(redis_client_async=mock_redis)
        b = FederatedLearningJobRedisEventConsumer.get_instance(redis_client_async=mock_redis)
        assert a is b

    def test_returns_non_none_instance(self):
        assert FederatedLearningJobRedisEventConsumer.get_instance(redis_client_async=MagicMock()) is not None


class TestStartRedisEventConsumer:
    async def test_processes_success_message_and_updates_job(self, consumer):
        from entities import FederatedLearningJobModel

        job = FederatedLearningJobModel()
        job.id = 1
        job.status = FederatedLearningJobStatus.IN_PROGRESS

        dto = CeleryJobDTO(job_id="task-1", result_type=CeleryJobResultType.SUCCESS)
        message = {"type": "message", "data": dto.model_dump_json()}

        mock_pubsub = AsyncMock()
        mock_pubsub.subscribe = AsyncMock()
        mock_pubsub.unsubscribe = AsyncMock()
        mock_pubsub.close = AsyncMock()
        mock_pubsub.listen = MagicMock(return_value=_async_iter([message]))

        consumer._FederatedLearningJobRedisEventConsumer__redis_client_async.pubsub = MagicMock(
            return_value=mock_pubsub
        )

        mock_repo = AsyncMock()
        mock_repo.get_by_celery_task_id = AsyncMock(return_value=job)
        mock_repo.save = AsyncMock(return_value=job)

        mock_session = AsyncMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("services.federated_learning_job.redis.federated_learning_job_redis_event_consumer.DatabaseConnector.get_session_factory") as mock_factory, \
             patch("services.federated_learning_job.redis.federated_learning_job_redis_event_consumer.build_federated_learning_job_repository", return_value=mock_repo):
            mock_factory.return_value = MagicMock(return_value=mock_session)
            await consumer.start_redis_event_consumer()

        assert job.status == FederatedLearningJobStatus.SUCCESS

    async def test_processes_failure_message_and_updates_job(self, consumer):
        from entities import FederatedLearningJobModel

        job = FederatedLearningJobModel()
        job.id = 2
        job.status = FederatedLearningJobStatus.IN_PROGRESS

        dto = CeleryJobDTO(job_id="task-2", result_type=CeleryJobResultType.FAILURE, error="err")
        message = {"type": "message", "data": dto.model_dump_json()}

        mock_pubsub = AsyncMock()
        mock_pubsub.subscribe = AsyncMock()
        mock_pubsub.unsubscribe = AsyncMock()
        mock_pubsub.close = AsyncMock()
        mock_pubsub.listen = MagicMock(return_value=_async_iter([message]))

        consumer._FederatedLearningJobRedisEventConsumer__redis_client_async.pubsub = MagicMock(
            return_value=mock_pubsub
        )

        mock_repo = AsyncMock()
        mock_repo.get_by_celery_task_id = AsyncMock(return_value=job)
        mock_repo.save = AsyncMock(return_value=job)

        mock_session = AsyncMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("services.federated_learning_job.redis.federated_learning_job_redis_event_consumer.DatabaseConnector.get_session_factory") as mock_factory, \
             patch("services.federated_learning_job.redis.federated_learning_job_redis_event_consumer.build_federated_learning_job_repository", return_value=mock_repo):
            mock_factory.return_value = MagicMock(return_value=mock_session)
            await consumer.start_redis_event_consumer()

        assert job.status == FederatedLearningJobStatus.FAILURE

    async def test_does_nothing_when_job_not_found(self, consumer):
        dto = CeleryJobDTO(job_id="missing", result_type=CeleryJobResultType.SUCCESS)
        message = {"type": "message", "data": dto.model_dump_json()}

        mock_pubsub = AsyncMock()
        mock_pubsub.subscribe = AsyncMock()
        mock_pubsub.unsubscribe = AsyncMock()
        mock_pubsub.close = AsyncMock()
        mock_pubsub.listen = MagicMock(return_value=_async_iter([message]))

        consumer._FederatedLearningJobRedisEventConsumer__redis_client_async.pubsub = MagicMock(
            return_value=mock_pubsub
        )

        mock_repo = AsyncMock()
        mock_repo.get_by_celery_task_id = AsyncMock(return_value=None)

        mock_session = AsyncMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("services.federated_learning_job.redis.federated_learning_job_redis_event_consumer.DatabaseConnector.get_session_factory") as mock_factory, \
             patch("services.federated_learning_job.redis.federated_learning_job_redis_event_consumer.build_federated_learning_job_repository", return_value=mock_repo):
            mock_factory.return_value = MagicMock(return_value=mock_session)
            await consumer.start_redis_event_consumer()

        mock_repo.save.assert_not_awaited()

    async def test_handles_processing_exception_gracefully(self, consumer):
        message = {"type": "message", "data": "invalid-json"}

        mock_pubsub = AsyncMock()
        mock_pubsub.subscribe = AsyncMock()
        mock_pubsub.unsubscribe = AsyncMock()
        mock_pubsub.close = AsyncMock()
        mock_pubsub.listen = MagicMock(return_value=_async_iter([message]))

        consumer._FederatedLearningJobRedisEventConsumer__redis_client_async.pubsub = MagicMock(
            return_value=mock_pubsub
        )

        await consumer.start_redis_event_consumer()

    async def test_skips_none_message(self, consumer):
        none_message = None
        valid_message = {"type": "message", "data": "invalid-json"}  # triggers exception path

        mock_pubsub = AsyncMock()
        mock_pubsub.subscribe = AsyncMock()
        mock_pubsub.unsubscribe = AsyncMock()
        mock_pubsub.close = AsyncMock()
        mock_pubsub.listen = MagicMock(return_value=_async_iter([none_message, valid_message]))

        consumer._FederatedLearningJobRedisEventConsumer__redis_client_async.pubsub = MagicMock(
            return_value=mock_pubsub
        )

        await consumer.start_redis_event_consumer()

    async def test_skips_non_message_type(self, consumer):
        subscribe_msg = {"type": "subscribe", "data": None}

        mock_pubsub = AsyncMock()
        mock_pubsub.subscribe = AsyncMock()
        mock_pubsub.unsubscribe = AsyncMock()
        mock_pubsub.close = AsyncMock()
        mock_pubsub.listen = MagicMock(return_value=_async_iter([subscribe_msg]))

        consumer._FederatedLearningJobRedisEventConsumer__redis_client_async.pubsub = MagicMock(
            return_value=mock_pubsub
        )

        with patch("services.federated_learning_job.redis.federated_learning_job_redis_event_consumer.build_federated_learning_job_repository") as mock_build:
            await consumer.start_redis_event_consumer()

        mock_build.assert_not_called()

    async def test_unsubscribes_on_completion(self, consumer):
        mock_pubsub = AsyncMock()
        mock_pubsub.subscribe = AsyncMock()
        mock_pubsub.unsubscribe = AsyncMock()
        mock_pubsub.close = AsyncMock()
        mock_pubsub.listen = MagicMock(return_value=_async_iter([]))

        consumer._FederatedLearningJobRedisEventConsumer__redis_client_async.pubsub = MagicMock(
            return_value=mock_pubsub
        )

        await consumer.start_redis_event_consumer()

        mock_pubsub.unsubscribe.assert_awaited_once()
        mock_pubsub.close.assert_awaited_once()


def _async_iter(items):
    async def _gen():
        for item in items:
            yield item
    return _gen()
