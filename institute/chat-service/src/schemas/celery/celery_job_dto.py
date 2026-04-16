from typing import Optional

from pydantic import BaseModel

from schemas.celery.celery_job_result_type import CeleryJobResultType
from .query_response_dto import QueryResponseDTO


class CeleryJobDTO(BaseModel):
    job_id: str
    result_type: CeleryJobResultType
    chat_id: int
    result: Optional[QueryResponseDTO] = None
    error: Optional[str] = None