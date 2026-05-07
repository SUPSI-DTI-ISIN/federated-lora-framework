import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from router.exceptions.exception_handlers import (
    _start_federated_learning_job_bad_request_handler,
    register_exception_handlers,
)
from schemas.exceptions import StartFederatedLearningJobFoundError


@pytest.fixture(scope="module")
def client():
    app = FastAPI()
    register_exception_handlers(app=app)

    @app.get("/raise-bad-request")
    async def raise_bad_request():
        raise StartFederatedLearningJobFoundError(federated_learning_job_id=42)

    return TestClient(app)


class TestRegisterExceptionHandlers:
    def test_start_job_error_returns_400(self, client):
        response = client.get("/raise-bad-request")
        assert response.status_code == 400
        assert response.json()["error"] == "Bad Request"
        assert "42" in response.json()["message"]


class TestHandlerFunctionsDirect:
    async def test_bad_request_handler_returns_400(self):
        response = await _start_federated_learning_job_bad_request_handler(
            MagicMock(), StartFederatedLearningJobFoundError(federated_learning_job_id=10)
        )
        assert response.status_code == 400
