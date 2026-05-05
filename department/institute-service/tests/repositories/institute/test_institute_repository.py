import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import SQLAlchemyError

from entities import InstituteModel
from repositories.institute.institute_repository import InstituteRepository


@pytest.fixture()
def session():
    return AsyncMock()


@pytest.fixture()
def repo(session):
    return InstituteRepository(db_session=session)


@pytest.fixture()
def institute_model():
    m = InstituteModel()
    m.id = 1
    m.name = "Test"
    m.url = "http://t.local"
    m.deletable = True
    m.updatable = True
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


class TestSave:
    async def test_success(self, repo, session, institute_model):
        result = await repo.save(institute_model=institute_model)

        session.add.assert_called_once_with(institute_model)
        session.commit.assert_awaited_once()
        session.refresh.assert_awaited_once_with(institute_model)
        assert result is institute_model

    async def test_rolls_back_on_error(self, repo, session, institute_model):
        session.commit = AsyncMock(side_effect=SQLAlchemyError("commit failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.save(institute_model=institute_model)

        session.rollback.assert_awaited_once()


class TestGetAll:
    async def test_returns_list(self, repo, session):
        models = [InstituteModel(), InstituteModel()]
        session.execute = AsyncMock(return_value=_make_execute_result(models))

        assert await repo.get_all() == models

    async def test_returns_empty_list(self, repo, session):
        session.execute = AsyncMock(return_value=_make_execute_result([]))

        assert await repo.get_all() == []

    async def test_propagates_sqlalchemy_error(self, repo, session):
        session.execute = AsyncMock(side_effect=SQLAlchemyError("query failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.get_all()


class TestGetById:
    async def test_returns_model_when_found(self, repo, session, institute_model):
        session.get = AsyncMock(return_value=institute_model)

        assert await repo.get_by_id(institute_id=1) is institute_model

    async def test_returns_none_when_not_found(self, repo, session):
        session.get = AsyncMock(return_value=None)

        assert await repo.get_by_id(institute_id=999) is None

    async def test_propagates_sqlalchemy_error(self, repo, session):
        session.get = AsyncMock(side_effect=SQLAlchemyError("get failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.get_by_id(institute_id=1)


class TestGetByName:
    async def test_returns_model_when_found(self, repo, session, institute_model):
        session.execute = AsyncMock(return_value=_make_execute_result(institute_model, use_first=True))

        assert await repo.get_by_name(institute_name="Test") is institute_model

    async def test_returns_none_when_not_found(self, repo, session):
        session.execute = AsyncMock(return_value=_make_execute_result(None, use_first=True))

        assert await repo.get_by_name(institute_name="Ghost") is None

    async def test_propagates_sqlalchemy_error(self, repo, session):
        session.execute = AsyncMock(side_effect=SQLAlchemyError("query failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.get_by_name(institute_name="X")


class TestDeleteInstituteById:
    async def test_success(self, repo, session, institute_model):
        await repo.delete_institute_by_id(institute_model=institute_model)

        session.delete.assert_awaited_once_with(institute_model)
        session.commit.assert_awaited_once()

    async def test_rolls_back_on_error(self, repo, session, institute_model):
        session.commit = AsyncMock(side_effect=SQLAlchemyError("delete failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.delete_institute_by_id(institute_model=institute_model)

        session.rollback.assert_awaited_once()
