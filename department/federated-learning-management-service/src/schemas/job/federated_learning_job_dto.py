from typing import Optional

from pydantic import BaseModel

from schemas.job.federated_learning_job_result_type import FederatedLearningJobResultType


class FederatedLearningJobDTO(BaseModel):
    job_id: str
    result_type: FederatedLearningJobResultType
    result: Optional[str] = None
    error: Optional[str] = None