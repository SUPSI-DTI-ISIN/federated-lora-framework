from fastapi import status, Depends, APIRouter
from shared_auth_library.entities import User
from sse_starlette import EventSourceResponse
from starlette.requests import Request

from auth import jwt_validator
from schemas.job import FederatedLearningJobStartResponseDTO
from services.job import JobServiceInterface
from services.sse import SseServiceInterface
from .dependencies import get_job_service, get_custom_ping, get_sse_service

router = APIRouter(prefix="/jobs")
tags = ["jobs"]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=FederatedLearningJobStartResponseDTO,
    tags=tags
)
async def start_federated_learning(
        job_service: JobServiceInterface = Depends(get_job_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    return job_service.start_federated_learning()


"""
@router.get("/{job_id}")
async def get_task_status(job_id: str):
    print(celery.control.inspect().active())
    task_result = AsyncResult(job_id, app=celery)
    print(task_result.status)
    if task_result.ready():
        return {"task_id": job_id, "status": "completed", "result": task_result.result}
    if task_result.successful():
        return {"task_id": job_id, "status": "successful", "result": task_result.result}
    elif task_result.failed():
        return {"task_id": job_id, "status": "failed"}
    else:
        return {"task_id": job_id, "status": "in progress"}
"""

@router.get("/sse")
async def job_events(request: Request, sse_service: SseServiceInterface = Depends(get_sse_service)):
    return EventSourceResponse(
        sse_service.generate_sse_events(request=request),
        ping=10,
        ping_message_factory=get_custom_ping
    )