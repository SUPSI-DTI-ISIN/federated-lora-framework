import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from entities import MessageModel, MessageRole
from schemas.message import MessageDTO, MessageCreationRequestDTO
from services.message.message_service import MessageService


def _model(id=1, chat_id=10, role=MessageRole.USER, content="Hello", model_key="model-v1", adapter_version=1):
    m = MessageModel()
    m.id = id
    m.chat_id = chat_id
    m.role = role
    m.content = content
    m.model_key = model_key
    m.adapter_version = adapter_version
    m.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return m


@pytest.fixture()
def repo():
    return AsyncMock()


@pytest.fixture()
def service(repo):
    return MessageService(message_repository=repo, conversation_history_limit=None)


@pytest.fixture()
def service_with_limit(repo):
    return MessageService(message_repository=repo, conversation_history_limit=5)


class TestCreateNewMessage:
    async def test_creates_and_returns_dto(self, service, repo):
        saved = _model(id=10, chat_id=1, content="Hello")
        repo.save_message = AsyncMock(return_value=saved)

        dto = await service.create_new_message(
            message_creation_request_dto=MessageCreationRequestDTO(
                chat_id=1,
                role=MessageRole.USER,
                content="Hello",
                model_key="model-v1",
                adapter_version=1,
            )
        )

        repo.save_message.assert_awaited_once()
        assert isinstance(dto, MessageDTO)
        assert dto.id == 10
        assert dto.content == "Hello"

    async def test_passes_all_fields_to_model(self, service, repo):
        saved = _model()
        repo.save_message = AsyncMock(return_value=saved)

        await service.create_new_message(
            message_creation_request_dto=MessageCreationRequestDTO(
                chat_id=5,
                role=MessageRole.ASSISTANT,
                content="Hi there",
                model_key="model-v2",
                adapter_version=3,
            )
        )

        call_arg: MessageModel = repo.save_message.call_args.kwargs["message_model"]
        assert call_arg.chat_id == 5
        assert call_arg.role == MessageRole.ASSISTANT
        assert call_arg.content == "Hi there"
        assert call_arg.model_key == "model-v2"
        assert call_arg.adapter_version == 3

    async def test_passes_none_adapter_version(self, service, repo):
        saved = _model(adapter_version=None)
        repo.save_message = AsyncMock(return_value=saved)

        await service.create_new_message(
            message_creation_request_dto=MessageCreationRequestDTO(
                chat_id=1,
                role=MessageRole.USER,
                content="Hello",
                model_key="model-v1",
                adapter_version=None,
            )
        )

        call_arg: MessageModel = repo.save_message.call_args.kwargs["message_model"]
        assert call_arg.adapter_version is None


class TestGetAllByChat:
    async def test_returns_list_of_dtos_without_limit(self, service, repo):
        repo.get_all_by_chat = AsyncMock(return_value=[_model(id=1), _model(id=2)])

        result = await service.get_all_by_chat(chat_id=10)

        repo.get_all_by_chat.assert_awaited_once_with(chat_id=10)
        repo.get_all_by_chat_with_limit.assert_not_awaited()
        assert len(result) == 2
        assert all(isinstance(d, MessageDTO) for d in result)

    async def test_returns_empty_list_without_limit(self, service, repo):
        repo.get_all_by_chat = AsyncMock(return_value=[])

        assert await service.get_all_by_chat(chat_id=10) == []

    async def test_uses_limit_when_set(self, service_with_limit, repo):
        repo.get_all_by_chat_with_limit = AsyncMock(return_value=[_model(id=1)])

        result = await service_with_limit.get_all_by_chat(chat_id=10)

        repo.get_all_by_chat_with_limit.assert_awaited_once_with(chat_id=10, limit=5)
        repo.get_all_by_chat.assert_not_awaited()
        assert len(result) == 1

    async def test_returns_empty_list_with_limit(self, service_with_limit, repo):
        repo.get_all_by_chat_with_limit = AsyncMock(return_value=[])

        assert await service_with_limit.get_all_by_chat(chat_id=10) == []
