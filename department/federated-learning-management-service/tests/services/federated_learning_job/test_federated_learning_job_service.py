import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from entities import FederatedLearningJobModel, FederatedLearningJobStatus
from schemas.celery import CeleryJobDTO, CeleryJobResultType
from schemas.exceptions import StartFederatedLearningJobFoundError
from schemas.federated_learning_job import FederatedLearningJobDTO
from services.federated_learning_job.federated_learning_job_service import FederatedLearningJobService


def _model(id=1, celery_task_id="task-1", status=FederatedLearningJobStatus.IN_PROGRESS):
    m = FederatedLearningJobModel()
    m.id = id
    m.celery_task_id = celery_task_id
    m.status = status
    m.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return m


@pytest.fixture()
def repo():
    return AsyncMock()


@pytest.fixture()
def service(repo):
    return FederatedLearningJobService(federated_learning_job_repository=repo)


class TestCreateFederatedLearningJob:
    async def test_creates_and_returns_dto(self, service, repo):
        saved = _model(id=10, celery_task_id="task-new")
        repo.save = AsyncMock(return_value=saved)

        dto = await service.create_federated_learning_job(celery_task_id="task-new")

        repo.save.assert_awaited_once()
        assert isinstance(dto, FederatedLearningJobDTO)
        assert dto.id == 10
        assert dto.celery_task_id == "task-new"

    async def test_passes_in_progress_status_to_model(self, service, repo):
        saved = _model(id=1)
        repo.save = AsyncMock(return_value=saved)

        await service.create_federated_learning_job(celery_task_id="t")

        call_arg: FederatedLearningJobModel = repo.save.call_args.kwargs["federated_learning_job_model"]
        assert call_arg.status == FederatedLearningJobStatus.IN_PROGRESS

    async def test_passes_celery_task_id_to_model(self, service, repo):
        saved = _model(celery_task_id="my-task")
        repo.save = AsyncMock(return_value=saved)

        await service.create_federated_learning_job(celery_task_id="my-task")

        call_arg: FederatedLearningJobModel = repo.save.call_args.kwargs["federated_learning_job_model"]
        assert call_arg.celery_task_id == "my-task"


class TestGetAllFederatedLearningJobs:
    async def test_returns_list_of_dtos(self, service, repo):
        repo.get_all = AsyncMock(return_value=[_model(id=1), _model(id=2, celery_task_id="t2")])

        result = await service.get_all_federated_learning_jobs()

        assert len(result) == 2
        assert all(isinstance(d, FederatedLearningJobDTO) for d in result)

    async def test_returns_empty_list(self, service, repo):
        repo.get_all = AsyncMock(return_value=[])

        assert await service.get_all_federated_learning_jobs() == []


class TestEnsureNoJobInProgress:
    async def test_does_not_raise_when_no_job_in_progress(self, service, repo):
        repo.get_by_status = AsyncMock(return_value=None)

        await service.ensure_no_job_in_progress()

    async def test_raises_when_job_in_progress(self, service, repo):
        repo.get_by_status = AsyncMock(return_value=_model(id=5))

        with pytest.raises(StartFederatedLearningJobFoundError) as exc_info:
            await service.ensure_no_job_in_progress()

        assert exc_info.value.federated_learning_job_id == 5


class TestUpdateJobStatusFromCelery:
    async def test_sets_success_status(self, service, repo):
        job = _model(id=1)
        repo.get_by_celery_task_id = AsyncMock(return_value=job)
        repo.save = AsyncMock(return_value=job)

        await service.update_job_status_from_celery(
            CeleryJobDTO(job_id="task-1", result_type=CeleryJobResultType.SUCCESS)
        )

        assert job.status == FederatedLearningJobStatus.SUCCESS
        repo.save.assert_awaited_once_with(federated_learning_job_model=job)

    async def test_sets_failure_status(self, service, repo):
        job = _model(id=1)
        repo.get_by_celery_task_id = AsyncMock(return_value=job)
        repo.save = AsyncMock(return_value=job)

        await service.update_job_status_from_celery(
            CeleryJobDTO(job_id="task-1", result_type=CeleryJobResultType.FAILURE, error="err")
        )

        assert job.status == FederatedLearningJobStatus.FAILURE

    async def test_does_nothing_when_job_not_found(self, service, repo):
        repo.get_by_celery_task_id = AsyncMock(return_value=None)

        await service.update_job_status_from_celery(
            CeleryJobDTO(job_id="missing", result_type=CeleryJobResultType.SUCCESS)
        )

        repo.save.assert_not_awaited()

    async def test_does_not_change_status_for_unknown_result_type(self, service, repo):
        from unittest.mock import MagicMock as MM
        job = _model(id=1)
        original_status = job.status
        repo.get_by_celery_task_id = AsyncMock(return_value=job)
        repo.save = AsyncMock(return_value=job)

        unknown_dto = CeleryJobDTO(job_id="task-1", result_type=CeleryJobResultType.SUCCESS)
        unknown_dto = unknown_dto.model_copy(update={"result_type": MM()})

        await service.update_job_status_from_celery(unknown_dto)

        assert job.status == original_status
