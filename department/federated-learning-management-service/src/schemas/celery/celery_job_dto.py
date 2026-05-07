from typing import Optional

from pydantic import BaseModel

from schemas.celery.celery_job_result_type import CeleryJobResultType

class CeleryJobDTO(BaseModel):
    job_id: str
    result_type: CeleryJobResultType
    result: Optional[str] = None
    error: Optional[str] = None