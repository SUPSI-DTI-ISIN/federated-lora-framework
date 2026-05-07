import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from router.exceptions.exception_handlers import (
    _institute_not_found_handler,
    _institute_with_name_not_found_handler,
    _institute_cannot_be_deleted_handler,
    register_exception_handlers,
)
from schemas.exceptions.institute_errors import (
    InstituteNotFoundError,
    InstituteNameNotFoundError,
    InstituteCannotBeDeletedError,
)


@pytest.fixture(scope="module")
def client():
    app = FastAPI()
    register_exception_handlers(app=app)

    @app.get("/raise-not-found")
    async def raise_not_found():
        raise InstituteNotFoundError(institute_id=42)

    @app.get("/raise-name-not-found")
    async def raise_name_not_found():
        raise InstituteNameNotFoundError(institute_name="Ghost")

    @app.get("/raise-cannot-delete")
    async def raise_cannot_delete():
        raise InstituteCannotBeDeletedError(institute_id=7)

    return TestClient(app)


class TestRegisterExceptionHandlers:
    def test_institute_not_found_returns_404(self, client):
        response = client.get("/raise-not-found")
        assert response.status_code == 404
        assert response.json()["error"] == "Not Found"
        assert response.json()["institute_id"] == 42

    def test_institute_name_not_found_returns_404(self, client):
        response = client.get("/raise-name-not-found")
        assert response.status_code == 404
        assert response.json()["error"] == "Not Found"
        assert response.json()["institute_name"] == "Ghost"

    def test_institute_cannot_be_deleted_returns_400(self, client):
        response = client.get("/raise-cannot-delete")
        assert response.status_code == 400
        assert response.json()["error"] == "Bad Request"
        assert response.json()["institute_id"] == 7


class TestHandlerFunctionsDirect:
    async def test_not_found_handler_returns_404(self):
        response = await _institute_not_found_handler(MagicMock(), InstituteNotFoundError(institute_id=10))
        assert response.status_code == 404

    async def test_name_not_found_handler_returns_404(self):
        response = await _institute_with_name_not_found_handler(MagicMock(), InstituteNameNotFoundError(institute_name="X"))
        assert response.status_code == 404

    async def test_cannot_be_deleted_handler_returns_400(self):
        response = await _institute_cannot_be_deleted_handler(MagicMock(), InstituteCannotBeDeletedError(institute_id=3))
        assert response.status_code == 400
