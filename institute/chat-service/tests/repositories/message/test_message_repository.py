import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import SQLAlchemyError

from entities import MessageModel, MessageRole
from repositories.message.message_repository import MessageRepository


@pytest.fixture()
def session():
    return AsyncMock()


@pytest.fixture()
def repo(session):
    return MessageRepository(db_session=session)


@pytest.fixture()
def message_model():
    m = MessageModel()
    m.id = 1
    m.chat_id = 10
    m.role = MessageRole.USER
    m.content = "Hello"
    m.model_key = "model-v1"
    m.adapter_version = 1
    m.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return m


def _make_execute_result(items, *, use_first=False):
    mock_scalars = MagicMock()
    if use_first:
        mock_scalars.first.return_value = items
    else:
        mock_scalars.all.return_value = items
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    return mock_result


class TestSaveMessage:
    async def test_success(self, repo, session, message_model):
        result = await repo.save_message(message_model=message_model)

        session.add.assert_called_once_with(message_model)
        session.commit.assert_awaited_once()
        session.refresh.assert_awaited_once_with(message_model)
        assert result is message_model

    async def test_rolls_back_on_error(self, repo, session, message_model):
        session.commit = AsyncMock(side_effect=SQLAlchemyError("commit failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.save_message(message_model=message_model)

        session.rollback.assert_awaited_once()


class TestGetAllByChat:
    async def test_returns_list(self, repo, session):
        models = [MessageModel(), MessageModel()]
        session.execute = AsyncMock(return_value=_make_execute_result(models))

        result = await repo.get_all_by_chat(chat_id=10)
        assert result == models

    async def test_returns_empty_list(self, repo, session):
        session.execute = AsyncMock(return_value=_make_execute_result([]))

        assert await repo.get_all_by_chat(chat_id=10) == []

    async def test_propagates_sqlalchemy_error(self, repo, session):
        session.execute = AsyncMock(side_effect=SQLAlchemyError("query failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.get_all_by_chat(chat_id=10)


class TestGetAllByChatWithLimit:
    async def test_returns_limited_list(self, repo, session):
        models = [MessageModel()]
        session.execute = AsyncMock(return_value=_make_execute_result(models))

        result = await repo.get_all_by_chat_with_limit(chat_id=10, limit=1)
        assert result == models

    async def test_returns_empty_list(self, repo, session):
        session.execute = AsyncMock(return_value=_make_execute_result([]))

        assert await repo.get_all_by_chat_with_limit(chat_id=10, limit=5) == []

    async def test_propagates_sqlalchemy_error(self, repo, session):
        session.execute = AsyncMock(side_effect=SQLAlchemyError("query failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.get_all_by_chat_with_limit(chat_id=10, limit=5)


class TestGetLatestByChat:
    async def test_returns_model_when_found(self, repo, session, message_model):
        session.execute = AsyncMock(
            return_value=_make_execute_result(message_model, use_first=True)
        )

        result = await repo.get_latest_by_chat(chat_id=10)
        assert result is message_model

    async def test_returns_none_when_not_found(self, repo, session):
        session.execute = AsyncMock(return_value=_make_execute_result(None, use_first=True))

        assert await repo.get_latest_by_chat(chat_id=10) is None

    async def test_propagates_sqlalchemy_error(self, repo, session):
        session.execute = AsyncMock(side_effect=SQLAlchemyError("query failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.get_latest_by_chat(chat_id=10)
