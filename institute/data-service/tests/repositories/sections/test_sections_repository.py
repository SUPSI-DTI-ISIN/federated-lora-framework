import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import SQLAlchemyError

from models import SectionModel
from repositories.sections.sections_repository import SectionsRepository


@pytest.fixture()
def session():
    return AsyncMock()


@pytest.fixture()
def repo(session):
    return SectionsRepository(db_session=session)


@pytest.fixture()
def section_model():
    m = SectionModel()
    m.id = 1
    m.document_id = 10
    m.title = "1. Introduction"
    m.content = "Some content"
    return m


class TestSaveSection:
    async def test_success(self, repo, session, section_model):
        result = await repo.save_section(section_model=section_model)

        session.add.assert_called_once_with(section_model)
        session.commit.assert_awaited_once()
        session.refresh.assert_awaited_once_with(section_model)
        assert result is section_model

    async def test_rolls_back_on_error(self, repo, session, section_model):
        session.commit = AsyncMock(side_effect=SQLAlchemyError("commit failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.save_section(section_model=section_model)

        session.rollback.assert_awaited_once()


class TestGetById:
    async def test_returns_model_when_found(self, repo, session, section_model):
        session.get = AsyncMock(return_value=section_model)

        assert await repo.get_by_id(section_id=1) is section_model

    async def test_returns_none_when_not_found(self, repo, session):
        session.get = AsyncMock(return_value=None)

        assert await repo.get_by_id(section_id=999) is None

    async def test_propagates_sqlalchemy_error(self, repo, session):
        session.get = AsyncMock(side_effect=SQLAlchemyError("get failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.get_by_id(section_id=1)


class TestDeleteSection:
    async def test_success(self, repo, session, section_model):
        await repo.delete_section(section_model=section_model)

        session.delete.assert_awaited_once_with(section_model)
        session.commit.assert_awaited_once()

    async def test_rolls_back_on_error(self, repo, session, section_model):
        session.commit = AsyncMock(side_effect=SQLAlchemyError("delete failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.delete_section(section_model=section_model)

        session.rollback.assert_awaited_once()
