import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import SQLAlchemyError

from entities import FederatedLearningJobModel, FederatedLearningJobStatus
from repositories.federated_learning_job.federated_learning_job_repository import FederatedLearningJobRepository


@pytest.fixture()
def session():
    return AsyncMock()


@pytest.fixture()
def repo(session):
    return FederatedLearningJobRepository(db_session=session)


@pytest.fixture()
def job_model():
    m = FederatedLearningJobModel()
    m.id = 1
    m.celery_task_id = "task-abc"
    m.status = FederatedLearningJobStatus.IN_PROGRESS
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
    async def test_success(self, repo, session, job_model):
        result = await repo.save(federated_learning_job_model=job_model)

        session.add.assert_called_once_with(job_model)
        session.commit.assert_awaited_once()
        session.refresh.assert_awaited_once_with(job_model)
        assert result is job_model

    async def test_rolls_back_on_error(self, repo, session, job_model):
        session.commit = AsyncMock(side_effect=SQLAlchemyError("commit failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.save(federated_learning_job_model=job_model)

        session.rollback.assert_awaited_once()


class TestGetAll:
    async def test_returns_list(self, repo, session):
        models = [FederatedLearningJobModel(), FederatedLearningJobModel()]
        session.execute = AsyncMock(return_value=_make_execute_result(models))

        assert await repo.get_all() == models

    async def test_returns_empty_list(self, repo, session):
        session.execute = AsyncMock(return_value=_make_execute_result([]))

        assert await repo.get_all() == []

    async def test_propagates_sqlalchemy_error(self, repo, session):
        session.execute = AsyncMock(side_effect=SQLAlchemyError("query failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.get_all()


class TestGetByStatus:
    async def test_returns_model_when_found(self, repo, session, job_model):
        session.execute = AsyncMock(
            return_value=_make_execute_result(job_model, use_first=True)
        )

        result = await repo.get_by_status(status=FederatedLearningJobStatus.IN_PROGRESS)
        assert result is job_model

    async def test_returns_none_when_not_found(self, repo, session):
        session.execute = AsyncMock(return_value=_make_execute_result(None, use_first=True))

        assert await repo.get_by_status(status=FederatedLearningJobStatus.IN_PROGRESS) is None

    async def test_propagates_sqlalchemy_error(self, repo, session):
        session.execute = AsyncMock(side_effect=SQLAlchemyError("query failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.get_by_status(status=FederatedLearningJobStatus.IN_PROGRESS)


class TestGetByCeleryTaskId:
    async def test_returns_model_when_found(self, repo, session, job_model):
        session.execute = AsyncMock(
            return_value=_make_execute_result(job_model, use_first=True)
        )

        assert await repo.get_by_celery_task_id(celery_task_id="task-abc") is job_model

    async def test_returns_none_when_not_found(self, repo, session):
        session.execute = AsyncMock(return_value=_make_execute_result(None, use_first=True))

        assert await repo.get_by_celery_task_id(celery_task_id="missing") is None

    async def test_propagates_sqlalchemy_error(self, repo, session):
        session.execute = AsyncMock(side_effect=SQLAlchemyError("query failed"))

        with pytest.raises(SQLAlchemyError):
            await repo.get_by_celery_task_id(celery_task_id="t")
