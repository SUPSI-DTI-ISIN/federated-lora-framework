from typing import List
from datetime import datetime, timezone

from entities import FederatedLearningJobModel, FederatedLearningJobStatus
from repositories.federated_learning_job import FederatedLearningJobRepositoryInterface
from schemas.celery import CeleryJobDTO, CeleryJobResultType
from schemas.exceptions import FederatedLearningJobNotFoundError, StartFederatedLearningJobFoundError
from schemas.federated_learning_job import FederatedLearningJobDTO
from .federated_learning_job_service_interface import FederatedLearningJobServiceInterface


class FederatedLearningJobService(FederatedLearningJobServiceInterface):
    def __init__(self, federated_learning_job_repository: FederatedLearningJobRepositoryInterface):
        self.__federated_learning_job_repository = federated_learning_job_repository

    async def create_federated_learning_job(self, celery_task_id: str) -> FederatedLearningJobDTO:
        new_federated_learning_job = FederatedLearningJobModel(
            celery_task_id=celery_task_id,
            status=FederatedLearningJobStatus.IN_PROGRESS,
            created_at=datetime.now(tz=timezone.utc)
        )

        new_federated_learning_job_created = await self.__federated_learning_job_repository.save(federated_learning_job_model=new_federated_learning_job)
        return FederatedLearningJobDTO.model_validate(new_federated_learning_job_created)

    async def get_federated_learning_job_by_id(self, federated_learning_job_id: int) -> FederatedLearningJobDTO:
        federated_learning_job = await self.__federated_learning_job_repository.get_by_id(federated_learning_job_id=federated_learning_job_id)

        if federated_learning_job is None:
            raise FederatedLearningJobNotFoundError(federated_learning_job_id=federated_learning_job_id)

        return FederatedLearningJobDTO.model_validate(federated_learning_job)

    async def get_all_federated_learning_jobs(self) -> List[FederatedLearningJobDTO]:
        federated_learning_jobs = await self.__federated_learning_job_repository.get_all()

        return [FederatedLearningJobDTO.model_validate(federated_learning_job) for federated_learning_job in federated_learning_jobs]

    async def ensure_no_job_in_progress(self) -> None:
        federated_learning_job = await self.__federated_learning_job_repository.get_by_status(
            status=FederatedLearningJobStatus.IN_PROGRESS
        )

        if federated_learning_job is not None:
            raise StartFederatedLearningJobFoundError(
                federated_learning_job_id=federated_learning_job.id
            )

    async def update_job_status_from_celery(self, celery_job_dto: CeleryJobDTO) -> None:
        federated_learning_job = await self.__federated_learning_job_repository.get_by_celery_task_id(
            celery_task_id=celery_job_dto.job_id
        )

        if federated_learning_job is None:
            return

        if celery_job_dto.result_type == CeleryJobResultType.SUCCESS:
            federated_learning_job.status = FederatedLearningJobStatus.SUCCESS
        elif celery_job_dto.result_type == CeleryJobResultType.FAILURE:
            federated_learning_job.status = FederatedLearningJobStatus.FAILURE

        await self.__federated_learning_job_repository.save(federated_learning_job_model=federated_learning_job)