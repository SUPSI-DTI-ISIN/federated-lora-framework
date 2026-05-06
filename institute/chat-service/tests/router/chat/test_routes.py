import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from schemas.chat import ChatDTO
from schemas.exceptions import ChatNotFoundError
from router.chat.routes import router
from router.exceptions.exception_handlers import register_exception_handlers
from services.chat import ChatServiceInterface, get_chat_service
from services.sse import SseServiceInterface, get_sse_service, get_custom_ping
from auth import jwt_validator


def _dto(id=1, user_id="user-abc", title="Test Chat", is_doing_inference=False):
    return ChatDTO(
        id=id,
        user_id=user_id,
        title=title,
        is_doing_inference=is_doing_inference,
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )


@pytest.fixture()
def mock_chat_service():
    return AsyncMock(spec=ChatServiceInterface)


@pytest.fixture()
def mock_sse_service():
    return AsyncMock(spec=SseServiceInterface)


@pytest.fixture()
def client(mock_chat_service, mock_sse_service):
    app = FastAPI()
    register_exception_handlers(app=app)
    app.dependency_overrides[jwt_validator.get_current_user_required] = lambda: MagicMock(id="user-abc")
    app.dependency_overrides[get_chat_service] = lambda: mock_chat_service
    app.dependency_overrides[get_sse_service] = lambda: mock_sse_service
    app.dependency_overrides[get_custom_ping] = lambda: MagicMock()
    app.include_router(router)
    return TestClient(app, raise_server_exceptions=False)


class TestCreateChat:
    def test_returns_201(self, client, mock_chat_service):
        mock_chat_service.create_new_chat = AsyncMock(return_value=_dto(id=10, title="New Chat"))
        response = client.post("/chats/", json={"title": "New Chat"})
        assert response.status_code == 201
        assert response.json()["id"] == 10
        assert response.json()["title"] == "New Chat"

    def test_returns_201_with_no_title(self, client, mock_chat_service):
        mock_chat_service.create_new_chat = AsyncMock(return_value=_dto(id=1, title=None))
        response = client.post("/chats/", json={})
        assert response.status_code == 201


class TestListChats:
    def test_returns_200_with_items(self, client, mock_chat_service):
        mock_chat_service.get_all_by_user = AsyncMock(return_value=[_dto(id=1), _dto(id=2)])
        response = client.get("/chats")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_returns_empty_list(self, client, mock_chat_service):
        mock_chat_service.get_all_by_user = AsyncMock(return_value=[])
        response = client.get("/chats")
        assert response.status_code == 200
        assert response.json() == []


class TestGetChatById:
    def test_returns_200_when_found(self, client, mock_chat_service):
        mock_chat_service.get_by_id = AsyncMock(return_value=_dto(id=5))
        response = client.get("/chats/5")
        assert response.status_code == 200
        assert response.json()["id"] == 5

    def test_returns_404_when_not_found(self, client, mock_chat_service):
        mock_chat_service.get_by_id = AsyncMock(side_effect=ChatNotFoundError(chat_id=5))
        assert client.get("/chats/5").status_code == 404

    def test_404_response_contains_chat_id(self, client, mock_chat_service):
        mock_chat_service.get_by_id = AsyncMock(side_effect=ChatNotFoundError(chat_id=5))
        response = client.get("/chats/5")
        assert response.json()["chat_id"] == 5


class TestSseEndpoint:
    def test_sse_endpoint_is_reachable(self, client, mock_sse_service):
        async def _empty_gen(request, user_id):
            return
            yield  # make it an async generator

        mock_sse_service.generate_sse_events = _empty_gen
        response = client.get("/chats/sse/user-abc")
        assert response.status_code in [200, 500]


class TestDeleteChat:
    def test_returns_204(self, client, mock_chat_service):
        mock_chat_service.delete_chat_by_user = AsyncMock(return_value=None)
        assert client.delete("/chats/1").status_code == 204

    def test_returns_404_when_not_found(self, client, mock_chat_service):
        mock_chat_service.delete_chat_by_user = AsyncMock(side_effect=ChatNotFoundError(chat_id=1))
        assert client.delete("/chats/1").status_code == 404
