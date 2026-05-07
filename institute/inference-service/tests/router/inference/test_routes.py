import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from schemas.inference import QueryRequestDTO
from router.inference.routes import router
from services.inference import InferenceServiceInterface, get_inference_service


@pytest.fixture()
def mock_service():
    return AsyncMock(spec=InferenceServiceInterface)


@pytest.fixture()
def client(mock_service):
    app = FastAPI()
    app.dependency_overrides[get_inference_service] = lambda: mock_service
    app.include_router(router)
    return TestClient(app, raise_server_exceptions=False)


def _request_payload(**kwargs):
    defaults = dict(
        user_id="u-1", chat_id=1, model_key="llama-3",
        adapter_version=None, prompt="What is AI?", conversation_history=[],
    )
    defaults.update(kwargs)
    return defaults


class TestQueryEndpoint:
    def test_returns_202_on_success(self, client, mock_service):
        mock_service.inference_model = AsyncMock(return_value="task-id-123")
        response = client.post("/inference", json=_request_payload())
        assert response.status_code == 202

    def test_calls_inference_service(self, client, mock_service):
        mock_service.inference_model = AsyncMock(return_value="task-id-123")
        client.post("/inference", json=_request_payload(prompt="Hello"))
        mock_service.inference_model.assert_awaited_once()

    def test_missing_required_field_returns_422(self, client):
        response = client.post("/inference", json={"user_id": "u-1"})
        assert response.status_code == 422

    def test_with_adapter_version(self, client, mock_service):
        mock_service.inference_model = AsyncMock(return_value="task-id-456")
        response = client.post("/inference", json=_request_payload(adapter_version=2))
        assert response.status_code == 202

    def test_with_conversation_history(self, client, mock_service):
        mock_service.inference_model = AsyncMock(return_value="task-id-789")
        payload = _request_payload(
            conversation_history=[{"role": "user", "content": "Previous message"}]
        )
        response = client.post("/inference", json=payload)
        assert response.status_code == 202

    def test_router_init_export(self):
        from router.inference import router as r
        assert r is not None

    def test_router_version(self):
        import router.inference as ri
        assert ri.__version__ == "1.0.0"
