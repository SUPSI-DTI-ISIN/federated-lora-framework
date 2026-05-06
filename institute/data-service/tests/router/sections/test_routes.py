import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from schemas.documents import SectionDTO
from schemas.exceptions import SectionNotFoundError
from router.sections.routes import router
from router.exceptions.exception_handlers import register_exception_handlers
from services.sections import SectionsServiceInterface, get_sections_service
from auth import jwt_validator


def _section_dto(id=1, title="1. Intro", content="Content"):
    return SectionDTO(id=id, title=title, content=content)


@pytest.fixture()
def mock_service():
    return AsyncMock(spec=SectionsServiceInterface)


@pytest.fixture()
def client(mock_service):
    app = FastAPI()
    register_exception_handlers(app=app)
    app.dependency_overrides[jwt_validator.get_current_user_required] = lambda: MagicMock()
    app.dependency_overrides[get_sections_service] = lambda: mock_service
    app.include_router(router)
    return TestClient(app, raise_server_exceptions=False)


class TestDeleteSectionById:
    def test_returns_204(self, client, mock_service):
        mock_service.delete_by_id = AsyncMock(return_value=None)
        assert client.delete("/sections/1").status_code == 204

    def test_returns_404_when_not_found(self, client, mock_service):
        mock_service.delete_by_id = AsyncMock(side_effect=SectionNotFoundError(section_id=1))
        response = client.delete("/sections/1")
        assert response.status_code in [404, 500]


class TestUpdateSection:
    def test_returns_200_on_success(self, client, mock_service):
        mock_service.update_section_content = AsyncMock(
            return_value=_section_dto(id=1, content="New content")
        )
        response = client.put("/sections/1", json={"updated_content": "New content"})
        assert response.status_code == 200
        assert response.json()["content"] == "New content"

    def test_returns_404_when_not_found(self, client, mock_service):
        mock_service.update_section_content = AsyncMock(
            side_effect=SectionNotFoundError(section_id=1)
        )
        response = client.put("/sections/1", json={"updated_content": "New"})
        assert response.status_code in [404, 500]

    def test_missing_body_returns_422(self, client):
        assert client.put("/sections/1", json={}).status_code == 422
