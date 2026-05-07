import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from entities import ChatModel
from schemas.chat import ChatDTO, ChatCreationRequestDTO
from schemas.exceptions import ChatNotFoundError
from services.chat.chat_service import ChatService


def _model(id=1, user_id="user-abc", title="Test Chat", is_doing_inference=False):
    m = ChatModel()
    m.id = id
    m.user_id = user_id
    m.title = title
    m.is_doing_inference = is_doing_inference
    m.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    m.updated_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return m


@pytest.fixture()
def repo():
    return AsyncMock()


@pytest.fixture()
def service(repo):
    return ChatService(chat_repository=repo)


class TestCreateNewChat:
    async def test_creates_and_returns_dto(self, service, repo):
        saved = _model(id=10, user_id="u-1", title="New Chat")
        repo.save_chat = AsyncMock(return_value=saved)

        dto = await service.create_new_chat(
            chat_creation_request_dto=ChatCreationRequestDTO(title="New Chat"),
            user_id="u-1"
        )

        repo.save_chat.assert_awaited_once()
        assert isinstance(dto, ChatDTO)
        assert dto.id == 10
        assert dto.user_id == "u-1"
        assert dto.title == "New Chat"

    async def test_passes_user_id_to_model(self, service, repo):
        saved = _model(user_id="u-xyz")
        repo.save_chat = AsyncMock(return_value=saved)

        await service.create_new_chat(
            chat_creation_request_dto=ChatCreationRequestDTO(),
            user_id="u-xyz"
        )

        call_arg: ChatModel = repo.save_chat.call_args.kwargs["chat_model"]
        assert call_arg.user_id == "u-xyz"

    async def test_passes_title_to_model(self, service, repo):
        saved = _model(title="My Title")
        repo.save_chat = AsyncMock(return_value=saved)

        await service.create_new_chat(
            chat_creation_request_dto=ChatCreationRequestDTO(title="My Title"),
            user_id="u-1"
        )

        call_arg: ChatModel = repo.save_chat.call_args.kwargs["chat_model"]
        assert call_arg.title == "My Title"

    async def test_sets_is_doing_inference_to_false(self, service, repo):
        saved = _model()
        repo.save_chat = AsyncMock(return_value=saved)

        await service.create_new_chat(
            chat_creation_request_dto=ChatCreationRequestDTO(),
            user_id="u-1"
        )

        call_arg: ChatModel = repo.save_chat.call_args.kwargs["chat_model"]
        assert call_arg.is_doing_inference is False


class TestUpdateChatModificationDate:
    async def test_updates_and_returns_dto(self, service, repo):
        chat = _model(id=1)
        repo.get_by_id = AsyncMock(return_value=chat)
        repo.save_chat = AsyncMock(return_value=chat)

        dto = await service.update_chat_modification_date(chat_id=1)

        repo.save_chat.assert_awaited_once_with(chat_model=chat)
        assert isinstance(dto, ChatDTO)

    async def test_raises_not_found_when_missing(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(ChatNotFoundError) as exc_info:
            await service.update_chat_modification_date(chat_id=99)

        assert exc_info.value.chat_id == 99

    async def test_updates_updated_at_field(self, service, repo):
        old_time = datetime(2020, 1, 1, tzinfo=timezone.utc)
        chat = _model(id=1)
        chat.updated_at = old_time
        repo.get_by_id = AsyncMock(return_value=chat)
        repo.save_chat = AsyncMock(return_value=chat)

        await service.update_chat_modification_date(chat_id=1)

        assert chat.updated_at > old_time


class TestUpdateChatInferenceState:
    async def test_sets_inference_state_to_true(self, service, repo):
        chat = _model(id=1, is_doing_inference=False)
        repo.get_by_id = AsyncMock(return_value=chat)
        repo.save_chat = AsyncMock(return_value=chat)

        await service.update_chat_inference_state(chat_id=1, is_doing_inference=True)

        assert chat.is_doing_inference is True
        repo.save_chat.assert_awaited_once_with(chat_model=chat)

    async def test_sets_inference_state_to_false(self, service, repo):
        chat = _model(id=1, is_doing_inference=True)
        repo.get_by_id = AsyncMock(return_value=chat)
        repo.save_chat = AsyncMock(return_value=chat)

        await service.update_chat_inference_state(chat_id=1, is_doing_inference=False)

        assert chat.is_doing_inference is False

    async def test_raises_not_found_when_missing(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(ChatNotFoundError) as exc_info:
            await service.update_chat_inference_state(chat_id=99, is_doing_inference=True)

        assert exc_info.value.chat_id == 99

    async def test_returns_dto(self, service, repo):
        chat = _model(id=1)
        repo.get_by_id = AsyncMock(return_value=chat)
        repo.save_chat = AsyncMock(return_value=chat)

        dto = await service.update_chat_inference_state(chat_id=1, is_doing_inference=True)

        assert isinstance(dto, ChatDTO)


class TestGetAllByUser:
    async def test_returns_list_of_dtos(self, service, repo):
        repo.get_all_by_user = AsyncMock(return_value=[_model(id=1), _model(id=2)])

        result = await service.get_all_by_user(user_id="user-abc")

        assert len(result) == 2
        assert all(isinstance(d, ChatDTO) for d in result)

    async def test_returns_empty_list(self, service, repo):
        repo.get_all_by_user = AsyncMock(return_value=[])

        assert await service.get_all_by_user(user_id="user-abc") == []


class TestGetById:
    async def test_returns_dto_when_found(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=_model(id=5))

        dto = await service.get_by_id(chat_id=5)

        assert isinstance(dto, ChatDTO)
        assert dto.id == 5

    async def test_raises_not_found_when_missing(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(ChatNotFoundError) as exc_info:
            await service.get_by_id(chat_id=999)

        assert exc_info.value.chat_id == 999


class TestDeleteChatByUser:
    async def test_deletes_successfully(self, service, repo):
        chat = _model(id=1)
        repo.get_by_id = AsyncMock(return_value=chat)

        await service.delete_chat_by_user(chat_id=1)

        repo.delete_chat_by_user.assert_awaited_once_with(chat_model=chat)

    async def test_raises_not_found_when_missing(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(ChatNotFoundError) as exc_info:
            await service.delete_chat_by_user(chat_id=99)

        assert exc_info.value.chat_id == 99
