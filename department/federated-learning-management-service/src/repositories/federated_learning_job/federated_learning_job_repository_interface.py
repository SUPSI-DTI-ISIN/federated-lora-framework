from abc import ABC, abstractmethod
from typing import List, Optional

from entities import FederatedLearningJobModel, FederatedLearningJobStatus


class FederatedLearningJobRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, federated_learning_job_model: FederatedLearningJobModel) -> FederatedLearningJobModel:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[FederatedLearningJobModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_status(self, status: FederatedLearningJobStatus) -> Optional[FederatedLearningJobModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_celery_task_id(self, celery_task_id: str) -> Optional[FederatedLearningJobModel]:
        raise NotImplementedError