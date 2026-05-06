import json
import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

from entities import ChatModel, MessageRole
from schemas.celery import CeleryJobResultType, CeleryJobDTO, QueryResponseDTO
from schemas.exceptions import ChatNotFoundError
from services.inference.redis.inference_result_redis_event_consumer import InferenceResultRedisEventConsumer


@pytest.fixture(autouse=True)
def reset_singleton():
    InferenceResultRedisEventConsumer._InferenceResultRedisEventConsumer__INSTANCE = None
    yield
    InferenceResultRedisEventConsumer._InferenceResultRedisEventConsumer__INSTANCE = None


def _chat_model(id=1, is_doing_inference=True):
    m = ChatModel()
    m.id = id
    m.user_id = "u-1"
    m.title = "Test"
    m.is_doing_inference = is_doing_inference
    m.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    m.updated_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return m


def _success_dto(chat_id=1):
    return CeleryJobDTO(
        job_id="job-1",
        result_type=CeleryJobResultType.SUCCESS,
        chat_id=chat_id,
        result=QueryResponseDTO(
            user_id="u-1",
            chat_id=chat_id,
            prompt="Hello",
            response="Hi",
            model_key="model-v1",
            adapter_version=1,
        ),
    )


def _failure_dto(chat_id=1):
    return CeleryJobDTO(
        job_id="job-2",
        result_type=CeleryJobResultType.FAILURE,
        chat_id=chat_id,
        error="Something went wrong",
    )


@pytest.fixture()
def redis_client():
    return MagicMock()


@pytest.fixture()
def consumer(redis_client):
    return InferenceResultRedisEventConsumer(redis_client_async=redis_client)


class TestGetInstance:
    def test_returns_same_instance(self, redis_client):
        i1 = InferenceResultRedisEventConsumer.get_instance(redis_client_async=redis_client)
        i2 = InferenceResultRedisEventConsumer.get_instance(redis_client_async=redis_client)
        assert i1 is i2

    def test_creates_new_instance_after_reset(self, redis_client):
        i1 = InferenceResultRedisEventConsumer.get_instance(redis_client_async=redis_client)
        InferenceResultRedisEventConsumer._InferenceResultRedisEventConsumer__INSTANCE = None
        i2 = InferenceResultRedisEventConsumer.get_instance(redis_client_async=redis_client)
        assert i1 is not i2


class TestHandleAssistantInferenceMessage:
    async def test_success_creates_assistant_message_with_response(self, consumer):
        chat = _chat_model()
        dto = _success_dto(chat_id=1)

        mock_session = AsyncMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        mock_chat_repo = AsyncMock()
        mock_chat_repo.get_by_id = AsyncMock(return_value=chat)
        mock_chat_repo.save_chat = AsyncMock(return_value=chat)

        mock_msg_repo = AsyncMock()
        mock_msg_repo.save_message = AsyncMock()

        with patch("services.inference.redis.inference_result_redis_event_consumer.DatabaseConnector") as mock_db, \
             patch("services.inference.redis.inference_result_redis_event_consumer.build_chat_repository", return_value=mock_chat_repo), \
             patch("services.inference.redis.inference_result_redis_event_consumer.build_message_repository", return_value=mock_msg_repo):
            mock_db.get_session_factory = MagicMock(return_value=MagicMock(return_value=mock_session))

            await consumer._InferenceResultRedisEventConsumer__handle_assistant_inference_message(
                is_inference_failed=False,
                celery_job_dto=dto,
            )

        mock_msg_repo.save_message.assert_awaited_once()
        saved_msg = mock_msg_repo.save_message.call_args.kwargs["message_model"]
        assert saved_msg.role == MessageRole.ASSISTANT
        assert saved_msg.content == "Hi"

    async def test_failure_creates_error_assistant_message(self, consumer):
        chat = _chat_model()
        dto = _failure_dto(chat_id=1)

        mock_session = AsyncMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        mock_chat_repo = AsyncMock()
        mock_chat_repo.get_by_id = AsyncMock(return_value=chat)
        mock_chat_repo.save_chat = AsyncMock(return_value=chat)

        mock_msg_repo = AsyncMock()
        mock_msg_repo.save_message = AsyncMock()

        with patch("services.inference.redis.inference_result_redis_event_consumer.DatabaseConnector") as mock_db, \
             patch("services.inference.redis.inference_result_redis_event_consumer.build_chat_repository", return_value=mock_chat_repo), \
             patch("services.inference.redis.inference_result_redis_event_consumer.build_message_repository", return_value=mock_msg_repo):
            mock_db.get_session_factory = MagicMock(return_value=MagicMock(return_value=mock_session))

            await consumer._InferenceResultRedisEventConsumer__handle_assistant_inference_message(
                is_inference_failed=True,
                celery_job_dto=dto,
            )

        mock_msg_repo.save_message.assert_awaited_once()
        saved_msg = mock_msg_repo.save_message.call_args.kwargs["message_model"]
        assert saved_msg.role == MessageRole.ASSISTANT
        assert saved_msg.content == "Error during inference"

    async def test_skips_when_dto_is_none(self, consumer):
        await consumer._InferenceResultRedisEventConsumer__handle_assistant_inference_message(
            is_inference_failed=False,
            celery_job_dto=None,
        )

    async def test_update_chat_inference_state_raises_when_chat_not_found(self, consumer):
        mock_chat_repo = AsyncMock()
        mock_chat_repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(ChatNotFoundError) as exc_info:
            await consumer._InferenceResultRedisEventConsumer__update_chat_inference_state(
                chat_repository=mock_chat_repo,
                chat_id=99,
            )

        assert exc_info.value.chat_id == 99

    async def test_update_chat_inference_state_sets_false(self, consumer):
        chat = _chat_model(is_doing_inference=True)
        mock_chat_repo = AsyncMock()
        mock_chat_repo.get_by_id = AsyncMock(return_value=chat)
        mock_chat_repo.save_chat = AsyncMock(return_value=chat)

        await consumer._InferenceResultRedisEventConsumer__update_chat_inference_state(
            chat_repository=mock_chat_repo,
            chat_id=1,
        )

        assert chat.is_doing_inference is False
        mock_chat_repo.save_chat.assert_awaited_once_with(chat_model=chat)

    async def test_update_chat_modification_date_raises_when_chat_not_found(self, consumer):
        mock_chat_repo = AsyncMock()
        mock_chat_repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(ChatNotFoundError) as exc_info:
            await consumer._InferenceResultRedisEventConsumer__update_chat_modification_date(
                chat_repository=mock_chat_repo,
                chat_id=99,
            )

        assert exc_info.value.chat_id == 99

    async def test_update_chat_modification_date_updates_timestamp(self, consumer):
        old_time = datetime(2020, 1, 1, tzinfo=timezone.utc)
        chat = _chat_model()
        chat.updated_at = old_time
        mock_chat_repo = AsyncMock()
        mock_chat_repo.get_by_id = AsyncMock(return_value=chat)
        mock_chat_repo.save_chat = AsyncMock(return_value=chat)

        await consumer._InferenceResultRedisEventConsumer__update_chat_modification_date(
            chat_repository=mock_chat_repo,
            chat_id=1,
        )

        assert chat.updated_at > old_time
        mock_chat_repo.save_chat.assert_awaited_once_with(chat_model=chat)

    async def test_create_new_message_calls_save(self, consumer):
        from entities import MessageModel
        mock_msg_repo = AsyncMock()
        mock_msg_repo.save_message = AsyncMock()

        msg = MessageModel()
        msg.chat_id = 1
        msg.role = MessageRole.ASSISTANT
        msg.content = "Hi"
        msg.model_key = "model-v1"
        msg.adapter_version = 1
        msg.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)

        await consumer._InferenceResultRedisEventConsumer__create_new_message(
            message_repository=mock_msg_repo,
            message_model=msg,
        )

        mock_msg_repo.save_message.assert_awaited_once_with(message_model=msg)


class TestStartRedisEventConsumer:
    async def test_processes_success_message(self, consumer, redis_client):
        dto = _success_dto(chat_id=1)
        json_data = dto.model_dump_json()

        messages = [
            {"type": "psubscribe", "data": None},
            {"type": "pmessage", "data": json_data},
        ]

        async def _listen():
            for m in messages:
                yield m

        mock_pubsub = AsyncMock()
        mock_pubsub.psubscribe = AsyncMock()
        mock_pubsub.punsubscribe = AsyncMock()
        mock_pubsub.close = AsyncMock()
        mock_pubsub.listen = _listen
        redis_client.pubsub = MagicMock(return_value=mock_pubsub)

        chat = _chat_model()
        mock_session = AsyncMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        mock_chat_repo = AsyncMock()
        mock_chat_repo.get_by_id = AsyncMock(return_value=chat)
        mock_chat_repo.save_chat = AsyncMock(return_value=chat)

        mock_msg_repo = AsyncMock()
        mock_msg_repo.save_message = AsyncMock()

        with patch("services.inference.redis.inference_result_redis_event_consumer.DatabaseConnector") as mock_db, \
             patch("services.inference.redis.inference_result_redis_event_consumer.build_chat_repository", return_value=mock_chat_repo), \
             patch("services.inference.redis.inference_result_redis_event_consumer.build_message_repository", return_value=mock_msg_repo):
            mock_db.get_session_factory = MagicMock(return_value=MagicMock(return_value=mock_session))

            await consumer.start_redis_event_consumer()

        mock_pubsub.psubscribe.assert_awaited_once()
        mock_pubsub.punsubscribe.assert_awaited_once()
        mock_msg_repo.save_message.assert_awaited_once()

    async def test_processes_failure_message(self, consumer, redis_client):
        dto = _failure_dto(chat_id=1)
        json_data = dto.model_dump_json()

        messages = [
            {"type": "pmessage", "data": json_data},
        ]

        async def _listen():
            for m in messages:
                yield m

        mock_pubsub = AsyncMock()
        mock_pubsub.psubscribe = AsyncMock()
        mock_pubsub.punsubscribe = AsyncMock()
        mock_pubsub.close = AsyncMock()
        mock_pubsub.listen = _listen
        redis_client.pubsub = MagicMock(return_value=mock_pubsub)

        chat = _chat_model()
        mock_session = AsyncMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        mock_chat_repo = AsyncMock()
        mock_chat_repo.get_by_id = AsyncMock(return_value=chat)
        mock_chat_repo.save_chat = AsyncMock(return_value=chat)

        mock_msg_repo = AsyncMock()
        mock_msg_repo.save_message = AsyncMock()

        with patch("services.inference.redis.inference_result_redis_event_consumer.DatabaseConnector") as mock_db, \
             patch("services.inference.redis.inference_result_redis_event_consumer.build_chat_repository", return_value=mock_chat_repo), \
             patch("services.inference.redis.inference_result_redis_event_consumer.build_message_repository", return_value=mock_msg_repo):
            mock_db.get_session_factory = MagicMock(return_value=MagicMock(return_value=mock_session))

            await consumer.start_redis_event_consumer()

        mock_msg_repo.save_message.assert_awaited_once()
        saved_msg = mock_msg_repo.save_message.call_args.kwargs["message_model"]
        assert saved_msg.content == "Error during inference"

    async def test_skips_non_pmessage_types(self, consumer, redis_client):
        messages = [
            {"type": "psubscribe", "data": None},
            {"type": "subscribe", "data": None},
        ]

        async def _listen():
            for m in messages:
                yield m

        mock_pubsub = AsyncMock()
        mock_pubsub.psubscribe = AsyncMock()
        mock_pubsub.punsubscribe = AsyncMock()
        mock_pubsub.close = AsyncMock()
        mock_pubsub.listen = _listen
        redis_client.pubsub = MagicMock(return_value=mock_pubsub)

        with patch("services.inference.redis.inference_result_redis_event_consumer.DatabaseConnector"):
            await consumer.start_redis_event_consumer()

        mock_pubsub.punsubscribe.assert_awaited_once()

    async def test_skips_none_messages(self, consumer, redis_client):
        messages = [None]

        async def _listen():
            for m in messages:
                yield m

        mock_pubsub = AsyncMock()
        mock_pubsub.psubscribe = AsyncMock()
        mock_pubsub.punsubscribe = AsyncMock()
        mock_pubsub.close = AsyncMock()
        mock_pubsub.listen = _listen
        redis_client.pubsub = MagicMock(return_value=mock_pubsub)

        with patch("services.inference.redis.inference_result_redis_event_consumer.DatabaseConnector"):
            await consumer.start_redis_event_consumer()

        mock_pubsub.punsubscribe.assert_awaited_once()

    async def test_handles_exception_in_message_processing(self, consumer, redis_client):
        messages = [
            {"type": "pmessage", "data": "not-valid-json"},
        ]

        async def _listen():
            for m in messages:
                yield m

        mock_pubsub = AsyncMock()
        mock_pubsub.psubscribe = AsyncMock()
        mock_pubsub.punsubscribe = AsyncMock()
        mock_pubsub.close = AsyncMock()
        mock_pubsub.listen = _listen
        redis_client.pubsub = MagicMock(return_value=mock_pubsub)

        with patch("services.inference.redis.inference_result_redis_event_consumer.DatabaseConnector"):
            await consumer.start_redis_event_consumer()

        mock_pubsub.punsubscribe.assert_awaited_once()
