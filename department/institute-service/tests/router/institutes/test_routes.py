import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from schemas.institute import InstituteDTO, InstituteTrainingParticipationDTO
from schemas.exceptions.institute_errors import (
    InstituteNotFoundError,
    InstituteNameNotFoundError,
    InstituteCannotBeDeletedError,
)
from router.institutes.routes import router
from router.exceptions.exception_handlers import register_exception_handlers
from services.institute import InstituteServiceInterface, get_institute_service
from auth import jwt_validator


def _dto(id=1, name="Inst", url="http://inst.local", deletable=True, updatable=True):
    return InstituteDTO(id=id, name=name, url=url, deletable=deletable, updatable=updatable)


def _training_dto(id=1, name="Inst", samples=10, reachable=True):
    return InstituteTrainingParticipationDTO(
        id=id, institute_name=name, trainable_samples_number=samples, is_reachable=reachable
    )


@pytest.fixture()
def mock_service():
    return AsyncMock(spec=InstituteServiceInterface)


@pytest.fixture()
def client(mock_service):
    app = FastAPI()
    register_exception_handlers(app=app)
    app.dependency_overrides[jwt_validator.get_current_user_required] = lambda: MagicMock()
    app.dependency_overrides[get_institute_service] = lambda: mock_service
    app.include_router(router)
    return TestClient(app, raise_server_exceptions=False)


class TestCreateInstitute:
    def test_returns_201(self, client, mock_service):
        mock_service.create_new_institute = AsyncMock(return_value=_dto(id=10, name="New"))
        response = client.post("/institutes", json={"name": "New", "url": "http://new.local"})
        assert response.status_code == 201
        assert response.json()["id"] == 10

    def test_missing_body_returns_422(self, client):
        assert client.post("/institutes", json={}).status_code == 422


class TestUpdateInstitute:
    def test_returns_201(self, client, mock_service):
        mock_service.update_institute = AsyncMock(return_value=_dto(id=1, name="Updated"))
        response = client.put("/institutes/1", json={"name": "Updated"})
        assert response.status_code == 201
        assert response.json()["name"] == "Updated"

    def test_not_found_returns_404(self, client, mock_service):
        mock_service.update_institute = AsyncMock(side_effect=InstituteNotFoundError(institute_id=99))
        assert client.put("/institutes/99", json={"name": "X"}).status_code == 404


class TestListInstitutes:
    def test_returns_200_with_items(self, client, mock_service):
        mock_service.get_all = AsyncMock(return_value=[_dto(id=1), _dto(id=2, name="B")])
        response = client.get("/institutes")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_returns_empty_list(self, client, mock_service):
        mock_service.get_all = AsyncMock(return_value=[])
        response = client.get("/institutes")
        assert response.status_code == 200
        assert response.json() == []


class TestGetTrainingParticipation:
    def test_returns_200_with_data(self, client, mock_service):
        mock_service.get_institutes_training_participation = AsyncMock(
            return_value=[_training_dto(id=1, name="Alpha", samples=50)]
        )
        response = client.get("/institutes/training-participation")
        assert response.status_code == 200
        assert response.json()[0]["is_reachable"] is True


class TestGetInstituteById:
    def test_returns_200_when_found(self, client, mock_service):
        mock_service.get_by_id = AsyncMock(return_value=_dto(id=5))
        response = client.get("/institutes/5")
        assert response.status_code == 200
        assert response.json()["id"] == 5

    def test_returns_404_when_not_found(self, client, mock_service):
        mock_service.get_by_id = AsyncMock(side_effect=InstituteNotFoundError(institute_id=5))
        assert client.get("/institutes/5").status_code == 404


class TestGetInstituteByName:
    def test_returns_200_when_found(self, client, mock_service):
        mock_service.get_by_name = AsyncMock(return_value=_dto(name="Alpha"))
        response = client.get("/institutes/name/Alpha")
        assert response.status_code == 200
        assert response.json()["name"] == "Alpha"

    def test_returns_404_when_not_found(self, client, mock_service):
        mock_service.get_by_name = AsyncMock(side_effect=InstituteNameNotFoundError(institute_name="Ghost"))
        assert client.get("/institutes/name/Ghost").status_code == 404


class TestDeleteInstitute:
    def test_returns_204(self, client, mock_service):
        mock_service.delete_institute_by_id = AsyncMock(return_value=None)
        assert client.delete("/institutes/1").status_code == 204

    def test_not_found_returns_404(self, client, mock_service):
        mock_service.delete_institute_by_id = AsyncMock(side_effect=InstituteNotFoundError(institute_id=1))
        assert client.delete("/institutes/1").status_code == 404

    def test_cannot_be_deleted_returns_400(self, client, mock_service):
        mock_service.delete_institute_by_id = AsyncMock(side_effect=InstituteCannotBeDeletedError(institute_id=1))
        assert client.delete("/institutes/1").status_code == 400
