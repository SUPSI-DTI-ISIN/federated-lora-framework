import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

from entities import MessageRole
from schemas.chat import ConversationDTO
from schemas.exceptions import InferenceRequestError
from schemas.message import MessageDTO
from services.inference.inference_service import InferenceService


def _message_dto(id=1, chat_id=10, content="Hello", model_key="model-v1", adapter_version=1):
    return MessageDTO(
        id=id,
        chat_id=chat_id,
        role=MessageRole.USER.value,
        content=content,
        model_key=model_key,
        adapter_version=adapter_version,
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )


@pytest.fixture(autouse=True)
def reset_singleton():
    InferenceService._InferenceService__INSTANCE = None
    yield
    InferenceService._InferenceService__INSTANCE = None


@pytest.fixture()
def client():
    return AsyncMock()


@pytest.fixture()
def service(client):
    return InferenceService(inference_service_client=client)


class TestInferenceModel:
    async def test_returns_true_on_success(self, service, client):
        client.inference_model = AsyncMock(return_value=None)

        result = await service.inference_model(
            user_id="u-1",
            chat_id=10,
            user_message=_message_dto(),
            conversation_history=[],
        )

        assert result is True

    async def test_calls_client_with_correct_params(self, service, client):
        client.inference_model = AsyncMock(return_value=None)
        msg = _message_dto(chat_id=5, content="What is AI?", model_key="model-v2", adapter_version=3)
        history = [ConversationDTO(role="user", content="Previous")]

        await service.inference_model(
            user_id="u-xyz",
            chat_id=5,
            user_message=msg,
            conversation_history=history,
        )

        client.inference_model.assert_awaited_once()
        call_arg = client.inference_model.call_args.kwargs["query_request_dto"]
        assert call_arg.user_id == "u-xyz"
        assert call_arg.chat_id == 5
        assert call_arg.prompt == "What is AI?"
        assert call_arg.model_key == "model-v2"
        assert call_arg.adapter_version == 3
        assert len(call_arg.conversation_history) == 1

    async def test_raises_inference_request_error_on_runtime_error(self, service, client):
        client.inference_model = AsyncMock(side_effect=RuntimeError("connection refused"))

        with pytest.raises(InferenceRequestError) as exc_info:
            await service.inference_model(
                user_id="u-1",
                chat_id=10,
                user_message=_message_dto(),
                conversation_history=[],
            )

        assert "connection refused" in exc_info.value.detailed_err

    async def test_passes_empty_conversation_history(self, service, client):
        client.inference_model = AsyncMock(return_value=None)

        await service.inference_model(
            user_id="u-1",
            chat_id=10,
            user_message=_message_dto(),
            conversation_history=[],
        )

        call_arg = client.inference_model.call_args.kwargs["query_request_dto"]
        assert call_arg.conversation_history == []


class TestGetInstance:
    def test_returns_same_instance(self, client):
        instance1 = InferenceService.get_instance(inference_service_client=client)
        instance2 = InferenceService.get_instance(inference_service_client=client)
        assert instance1 is instance2

    def test_creates_new_instance_after_reset(self, client):
        instance1 = InferenceService.get_instance(inference_service_client=client)
        InferenceService._InferenceService__INSTANCE = None
        instance2 = InferenceService.get_instance(inference_service_client=client)
        assert instance1 is not instance2
