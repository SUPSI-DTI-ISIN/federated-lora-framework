from abc import ABC, abstractmethod
from typing import List

from schemas.celery import CeleryJobDTO
from schemas.federated_learning_job import FederatedLearningJobDTO


class FederatedLearningJobServiceInterface(ABC):
    @abstractmethod
    async def create_federated_learning_job(self, celery_task_id: str) -> FederatedLearningJobDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_all_federated_learning_jobs(self) -> List[FederatedLearningJobDTO]:
        raise NotImplementedError

    @abstractmethod
    async def get_federated_learning_job_by_id(self, federated_learning_job_id: int) -> FederatedLearningJobDTO:
        raise NotImplementedError

    @abstractmethod
    async def ensure_no_job_in_progress(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_job_status_from_celery(self, celery_job_dto: CeleryJobDTO) -> None:
        raise NotImplementedError