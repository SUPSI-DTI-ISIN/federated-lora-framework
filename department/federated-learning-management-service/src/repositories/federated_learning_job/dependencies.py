from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .federated_learning_job_repository_interface import FederatedLearningJobRepositoryInterface
from .federated_learning_job_repository import FederatedLearningJobRepository
from database import get_db_session

def get_federated_learning_job_repository(db: AsyncSession = Depends(get_db_session)) -> FederatedLearningJobRepositoryInterface:
    return FederatedLearningJobRepository(db_session=db)

def build_federated_learning_job_repository(db: AsyncSession) -> FederatedLearningJobRepositoryInterface:
    return FederatedLearningJobRepository(db_session=db)