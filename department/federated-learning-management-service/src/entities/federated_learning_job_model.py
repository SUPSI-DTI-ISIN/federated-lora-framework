from sqlalchemy import Integer, String, Column, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone


from .base_model import BaseModel
from .federated_learning_job_status_model import FederatedLearningJobStatus


class FederatedLearningJobModel(BaseModel):
    __tablename__ = "federated_learning_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    celery_task_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    status = Column(Enum(FederatedLearningJobStatus), nullable=False, default=FederatedLearningJobStatus.IN_PROGRESS)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)