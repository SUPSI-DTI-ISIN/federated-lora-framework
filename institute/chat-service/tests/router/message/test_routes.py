import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from entities import MessageRole
from schemas.message import MessageDTO
from schemas.exceptions import ChatNotFoundError, InferenceRequestError
from router.message.routes import router
from router.exceptions.exception_handlers import register_exception_handlers
from services.chat import ChatServiceInterface, get_chat_service
from services.message import MessageServiceInterface, get_message_service
from services.inference import InferenceServiceInterface, get_inference_service
from auth import jwt_validator


def _message_dto(id=1, chat_id=10, role=MessageRole.USER.value, content="Hello", model_key="model-v1", adapter_version=1):
    return MessageDTO(
        id=id,
        chat_id=chat_id,
        role=role,
        content=content,
        model_key=model_key,
        adapter_version=adapter_version,
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )


@pytest.fixture()
def mock_message_service():
    return AsyncMock(spec=MessageServiceInterface)


@pytest.fixture()
def mock_chat_service():
    return AsyncMock(spec=ChatServiceInterface)


@pytest.fixture()
def mock_inference_service():
    return AsyncMock(spec=InferenceServiceInterface)


@pytest.fixture()
def client(mock_message_service, mock_chat_service, mock_inference_service):
    app = FastAPI()
    register_exception_handlers(app=app)
    app.dependency_overrides[jwt_validator.get_current_user_required] = lambda: MagicMock(id="user-abc")
    app.dependency_overrides[get_message_service] = lambda: mock_message_service
    app.dependency_overrides[get_chat_service] = lambda: mock_chat_service
    app.dependency_overrides[get_inference_service] = lambda: mock_inference_service
    app.include_router(router)
    return TestClient(app, raise_server_exceptions=False)


class TestSendMessage:
    def test_returns_201_on_success(self, client, mock_message_service, mock_chat_service, mock_inference_service):
        user_msg = _message_dto(id=1, content="What is AI?")
        mock_message_service.create_new_message = AsyncMock(return_value=user_msg)
        mock_message_service.get_all_by_chat = AsyncMock(return_value=[user_msg])
        mock_inference_service.inference_model = AsyncMock(return_value=True)
        mock_chat_service.update_chat_inference_state = AsyncMock(return_value=MagicMock())
        mock_chat_service.update_chat_modification_date = AsyncMock(return_value=MagicMock())

        response = client.post(
            "/chats/10/messages",
            json={"model_key": "model-v1", "adapter_version": 1, "prompt": "What is AI?"},
        )

        assert response.status_code == 201
        assert response.json()["id"] == 1

    def test_missing_body_returns_422(self, client):
        assert client.post("/chats/10/messages", json={}).status_code == 422

    def test_returns_500_on_inference_error(self, client, mock_message_service, mock_chat_service, mock_inference_service):
        user_msg = _message_dto()
        mock_message_service.create_new_message = AsyncMock(return_value=user_msg)
        mock_message_service.get_all_by_chat = AsyncMock(return_value=[user_msg])
        mock_inference_service.inference_model = AsyncMock(
            side_effect=InferenceRequestError(detailed_err="timeout")
        )

        response = client.post(
            "/chats/10/messages",
            json={"model_key": "model-v1", "adapter_version": 1, "prompt": "Hello"},
        )

        assert response.status_code == 500
        assert response.json()["detailed_error"] == "timeout"

    def test_conversation_history_excludes_last_message(self, client, mock_message_service, mock_chat_service, mock_inference_service):
        msg1 = _message_dto(id=1, content="First")
        msg2 = _message_dto(id=2, content="Second")
        new_msg = _message_dto(id=3, content="Third")

        mock_message_service.create_new_message = AsyncMock(return_value=new_msg)
        mock_message_service.get_all_by_chat = AsyncMock(return_value=[msg1, msg2, new_msg])
        mock_inference_service.inference_model = AsyncMock(return_value=True)
        mock_chat_service.update_chat_inference_state = AsyncMock(return_value=MagicMock())
        mock_chat_service.update_chat_modification_date = AsyncMock(return_value=MagicMock())

        client.post(
            "/chats/10/messages",
            json={"model_key": "model-v1", "adapter_version": 1, "prompt": "Third"},
        )

        call_kwargs = mock_inference_service.inference_model.call_args.kwargs
        # conversation_history excludes the last message (the new user message)
        assert len(call_kwargs["conversation_history"]) == 2


class TestGetMessages:
    def test_returns_200_with_messages(self, client, mock_message_service):
        mock_message_service.get_all_by_chat = AsyncMock(
            return_value=[_message_dto(id=1), _message_dto(id=2)]
        )
        response = client.get("/chats/10/messages")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_returns_empty_list(self, client, mock_message_service):
        mock_message_service.get_all_by_chat = AsyncMock(return_value=[])
        response = client.get("/chats/10/messages")
        assert response.status_code == 200
        assert response.json() == []
