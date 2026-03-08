from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from entities import FederatedLearningJobModel, FederatedLearningJobStatus
from .federated_learning_job_repository_interface import FederatedLearningJobRepositoryInterface


class FederatedLearningJobRepository(FederatedLearningJobRepositoryInterface):
    def __init__(self, db_session: AsyncSession):
        self._db_session: AsyncSession = db_session

    async def save(self, federated_learning_job_model: FederatedLearningJobModel) -> FederatedLearningJobModel:
        try:
            self._db_session.add(federated_learning_job_model)
            await self._db_session.commit()
            await self._db_session.refresh(federated_learning_job_model)
            return federated_learning_job_model
        except SQLAlchemyError as exc:
            await self._db_session.rollback()
            raise exc

    async def get_all(self) -> List[FederatedLearningJobModel]:
        try:
            result = await self._db_session.execute(select(FederatedLearningJobModel))
            return list(result.scalars().all())
        except SQLAlchemyError as exc:
            raise exc

    async def get_by_id(self, federated_learning_job_id: int) -> Optional[FederatedLearningJobModel]:
        try:
            model = await self._db_session.get(FederatedLearningJobModel, federated_learning_job_id)
            return model
        except SQLAlchemyError as exc:
            raise exc

    async def get_by_status(self, status: FederatedLearningJobStatus) -> Optional[FederatedLearningJobModel]:
        try:
            stmt = select(FederatedLearningJobModel).where(
                FederatedLearningJobModel.status == status
            )

            result = await self._db_session.execute(stmt)
            return result.scalars().first()

        except SQLAlchemyError as exc:
            raise exc

    async def get_by_celery_task_id(self, celery_task_id: str) -> Optional[FederatedLearningJobModel]:
        try:
            stmt = select(FederatedLearningJobModel).where(
                FederatedLearningJobModel.celery_task_id == celery_task_id
            )

            result = await self._db_session.execute(stmt)
            return result.scalars().first()
        except SQLAlchemyError as exc:
            raise exc