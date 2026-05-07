import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from router.job.routes import router, get_federated_learning_job_service, get_celery_job_service, get_sse_service, get_custom_ping
from router.exceptions.exception_handlers import register_exception_handlers
from services.federated_learning_job import FederatedLearningJobServiceInterface
from services.celery import CeleryJobServiceInterface
from schemas.federated_learning_job import FederatedLearningJobDTO
from schemas.exceptions import StartFederatedLearningJobFoundError
from auth import jwt_validator


def _dto(id=1, celery_task_id="task-1", status="in_progress"):
    return FederatedLearningJobDTO(
        id=id,
        celery_task_id=celery_task_id,
        status=status,
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )


def _make_client(mock_job_svc, mock_celery_svc=None, mock_sse_svc=None):
    app = FastAPI()
    register_exception_handlers(app=app)
    app.dependency_overrides[jwt_validator.get_current_user_required] = lambda: MagicMock()
    app.dependency_overrides[get_federated_learning_job_service] = lambda: mock_job_svc
    if mock_celery_svc is not None:
        app.dependency_overrides[get_celery_job_service] = lambda: mock_celery_svc
    if mock_sse_svc is not None:
        app.dependency_overrides[get_sse_service] = lambda: mock_sse_svc
        app.dependency_overrides[get_custom_ping] = lambda: MagicMock()
    app.include_router(router)
    return TestClient(app, raise_server_exceptions=False)


class TestStartFederatedLearning:
    def test_returns_201_with_dto(self, mock_job_service, mock_celery_service):
        mock_celery_service.start_federated_learning = MagicMock(return_value="task-new")
        mock_job_service.ensure_no_job_in_progress = AsyncMock()
        mock_job_service.create_federated_learning_job = AsyncMock(return_value=_dto(id=10, celery_task_id="task-new"))

        response = _make_client(mock_job_service, mock_celery_service).post("/jobs")

        assert response.status_code == 201
        assert response.json()["id"] == 10
        assert response.json()["celery_task_id"] == "task-new"

    def test_calls_ensure_no_job_in_progress(self, mock_job_service, mock_celery_service):
        mock_celery_service.start_federated_learning = MagicMock(return_value="t")
        mock_job_service.ensure_no_job_in_progress = AsyncMock()
        mock_job_service.create_federated_learning_job = AsyncMock(return_value=_dto())

        _make_client(mock_job_service, mock_celery_service).post("/jobs")

        mock_job_service.ensure_no_job_in_progress.assert_awaited_once()

    def test_returns_400_when_job_already_in_progress(self, mock_job_service, mock_celery_service):
        mock_job_service.ensure_no_job_in_progress = AsyncMock(
            side_effect=StartFederatedLearningJobFoundError(federated_learning_job_id=5)
        )

        response = _make_client(mock_job_service, mock_celery_service).post("/jobs")

        assert response.status_code == 400
        assert "5" in response.json()["message"]


class TestGetAllFederatedLearningJobs:
    def test_returns_200_with_items(self, mock_job_service):
        mock_job_service.get_all_federated_learning_jobs = AsyncMock(
            return_value=[_dto(id=1), _dto(id=2, celery_task_id="t2")]
        )

        response = _make_client(mock_job_service).get("/jobs")

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_returns_empty_list(self, mock_job_service):
        mock_job_service.get_all_federated_learning_jobs = AsyncMock(return_value=[])

        response = _make_client(mock_job_service).get("/jobs")

        assert response.status_code == 200
        assert response.json() == []


class TestJobSseEndpoint:
    def test_sse_endpoint_exists(self, mock_job_service, mock_sse_service):
        async def _fake_generate(request):
            return
            yield  # make it an async generator

        mock_sse_service.generate_sse_events = _fake_generate
        client = _make_client(mock_job_service, mock_sse_svc=mock_sse_service)
        routes = [r.path for r in client.app.routes]
        assert any("sse" in p for p in routes)
