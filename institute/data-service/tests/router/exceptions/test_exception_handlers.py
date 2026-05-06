import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi import APIRouter, status

from schemas.exceptions import DocumentNotFoundError, DocumentAlreadyExistsError, InvalidFileError
from router.exceptions.exception_handlers import register_exception_handlers


def _make_client(*raise_exceptions):
    """Build a test client with routes that raise the given exceptions."""
    app = FastAPI()
    register_exception_handlers(app=app)
    router = APIRouter()

    for exc in raise_exceptions:
        exc_instance = exc  # capture

        @router.get(f"/raise/{type(exc_instance).__name__.lower()}")
        async def _raise(e=exc_instance):
            raise e

    app.include_router(router)
    return TestClient(app, raise_server_exceptions=False)


class TestDocumentNotFoundHandler:
    def test_returns_404(self):
        client = _make_client(DocumentNotFoundError(document_id=42))
        response = client.get("/raise/documentnotfounderror")
        assert response.status_code == 404

    def test_response_contains_document_id(self):
        client = _make_client(DocumentNotFoundError(document_id=42))
        response = client.get("/raise/documentnotfounderror")
        assert response.json()["document_id"] == 42

    def test_response_contains_error_field(self):
        client = _make_client(DocumentNotFoundError(document_id=1))
        response = client.get("/raise/documentnotfounderror")
        assert response.json()["error"] == "Not Found"


class TestDocumentAlreadyExistsHandler:
    def test_returns_409(self):
        client = _make_client(DocumentAlreadyExistsError(document_id=7))
        response = client.get("/raise/documentalreadyexistserror")
        assert response.status_code == 409

    def test_response_contains_document_id(self):
        client = _make_client(DocumentAlreadyExistsError(document_id=7))
        response = client.get("/raise/documentalreadyexistserror")
        assert response.json()["document_id"] == 7

    def test_response_contains_error_field(self):
        client = _make_client(DocumentAlreadyExistsError(document_id=1))
        response = client.get("/raise/documentalreadyexistserror")
        assert response.json()["error"] == "Conflict"


class TestInvalidFileHandler:
    def test_returns_400(self):
        client = _make_client(InvalidFileError(message="bad file"))
        response = client.get("/raise/invalidfileerror")
        assert response.status_code == 400

    def test_response_contains_error_field(self):
        client = _make_client(InvalidFileError(message="bad file"))
        response = client.get("/raise/invalidfileerror")
        assert response.json()["error"] == "Bad Request"
