from typing import List

from fastapi import status, Depends, APIRouter
from shared_auth_library.entities import User
from sse_starlette import EventSourceResponse
from starlette.requests import Request

from .dependencies_sse import get_sse_service, get_custom_ping
from .dependencies import get_federated_learning_job_service, get_celery_job_service
from services.sse import SseServiceInterface
from schemas.federated_learning_job import FederatedLearningJobDTO
from services.federated_learning_job import FederatedLearningJobServiceInterface
from services.celery import CeleryJobServiceInterface
from auth import jwt_validator

router = APIRouter(prefix="/jobs")
tags = ["jobs"]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=FederatedLearningJobDTO,
    tags=tags
)
async def start_federated_learning(
        celery_job_service: CeleryJobServiceInterface = Depends(get_celery_job_service),
        federated_learning_job_service: FederatedLearningJobServiceInterface = Depends(get_federated_learning_job_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    await federated_learning_job_service.ensure_no_job_in_progress()
    celery_task_id = celery_job_service.start_federated_learning()
    return await federated_learning_job_service.create_federated_learning_job(celery_task_id=celery_task_id)


@router.get(
    "/{job_id}",
    status_code=status.HTTP_200_OK,
    response_model=FederatedLearningJobDTO,
    tags=tags
)
async def get_federated_learning_job_by_id(
        job_id: int,
        federated_learning_job_service: FederatedLearningJobServiceInterface = Depends(get_federated_learning_job_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    return await federated_learning_job_service.get_federated_learning_job_by_id(federated_learning_job_id=job_id)

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[FederatedLearningJobDTO],
    tags=tags
)
async def get_all_federated_learning_job(
        federated_learning_job_service: FederatedLearningJobServiceInterface = Depends(get_federated_learning_job_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    return await federated_learning_job_service.get_all_federated_learning_jobs()

@router.get("/sse")
async def job_events(request: Request, sse_service: SseServiceInterface = Depends(get_sse_service)):
    return EventSourceResponse(
        sse_service.generate_sse_events(request=request),
        ping=10,
        ping_message_factory=get_custom_ping
    )