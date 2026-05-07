from pydantic import BaseModel, ConfigDict
from datetime import datetime

class FederatedLearningJobDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    celery_task_id: str
    status: str
    created_at: datetime