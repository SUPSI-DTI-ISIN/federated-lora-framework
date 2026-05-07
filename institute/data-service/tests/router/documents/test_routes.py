import io
import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from schemas.documents import DocumentDTO, SectionDTO, TrainingSamplesDTO
from schemas.exceptions import DocumentNotFoundError, DocumentAlreadyExistsError, InvalidFileError
from router.documents.routes import router
from router.exceptions.exception_handlers import register_exception_handlers
from services.documents import DocumentsServiceInterface, get_documents_service
from auth import jwt_validator


def _dto(id=1, number="DOC-001", title="Test Doc", is_trainable=False,
         is_externally_approved=False, sections=None):
    return DocumentDTO(
        id=id,
        number=number,
        title=title,
        is_trainable=is_trainable,
        is_externally_approved=is_externally_approved,
        sections=sections or [],
    )


@pytest.fixture()
def mock_service():
    return AsyncMock(spec=DocumentsServiceInterface)


@pytest.fixture()
def client(mock_service):
    app = FastAPI()
    register_exception_handlers(app=app)
    app.dependency_overrides[jwt_validator.get_current_user_required] = lambda: MagicMock()
    app.dependency_overrides[get_documents_service] = lambda: mock_service
    app.include_router(router)
    return TestClient(app, raise_server_exceptions=False)


class TestUpload:
    def test_returns_201_on_success(self, client, mock_service):
        mock_service.upload_data = AsyncMock(return_value=_dto(id=10))
        pdf_bytes = b"%PDF-1.4 fake content"
        response = client.post(
            "/documents/upload",
            data={"is_externally_approved": "false"},
            files={"file": ("test.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
        )
        assert response.status_code == 201
        assert response.json()["id"] == 10

    def test_returns_400_for_non_pdf(self, client, mock_service):
        response = client.post(
            "/documents/upload",
            data={"is_externally_approved": "false"},
            files={"file": ("test.txt", io.BytesIO(b"text content"), "text/plain")},
        )
        assert response.status_code == 400

    def test_returns_409_when_document_already_exists(self, client, mock_service):
        mock_service.upload_data = AsyncMock(side_effect=DocumentAlreadyExistsError(document_id=5))
        pdf_bytes = b"%PDF-1.4 fake content"
        response = client.post(
            "/documents/upload",
            data={"is_externally_approved": "false"},
            files={"file": ("test.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
        )
        assert response.status_code == 409

    def test_returns_400_when_invalid_file(self, client, mock_service):
        mock_service.upload_data = AsyncMock(side_effect=InvalidFileError(message="bad file"))
        pdf_bytes = b"%PDF-1.4 fake content"
        response = client.post(
            "/documents/upload",
            data={"is_externally_approved": "false"},
            files={"file": ("test.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
        )
        assert response.status_code == 400

    def test_passes_is_externally_approved_to_service(self, client, mock_service):
        mock_service.upload_data = AsyncMock(return_value=_dto(id=1, is_externally_approved=True))
        pdf_bytes = b"%PDF-1.4 fake content"
        client.post(
            "/documents/upload",
            data={"is_externally_approved": "true"},
            files={"file": ("test.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
        )
        call_kwargs = mock_service.upload_data.call_args.kwargs
        assert call_kwargs["is_externally_approved"] is True


class TestGetAll:
    def test_returns_200_with_items(self, client, mock_service):
        mock_service.get_all = AsyncMock(return_value=[_dto(id=1), _dto(id=2)])
        response = client.get("/documents")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_returns_empty_list(self, client, mock_service):
        mock_service.get_all = AsyncMock(return_value=[])
        response = client.get("/documents")
        assert response.status_code == 200
        assert response.json() == []


class TestGetAllTrainable:
    def test_returns_200_with_trainable_items(self, client, mock_service):
        mock_service.get_all_trainable = AsyncMock(return_value=[_dto(id=1, is_trainable=True)])
        response = client.get("/documents/trainable")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_returns_empty_list(self, client, mock_service):
        mock_service.get_all_trainable = AsyncMock(return_value=[])
        response = client.get("/documents/trainable")
        assert response.status_code == 200
        assert response.json() == []


class TestGetTrainingSamples:
    def test_returns_200_with_training_samples(self, client, mock_service):
        mock_service.get_training_samples = AsyncMock(
            return_value=TrainingSamplesDTO(institute_name="TestInstitute", trainable_samples_number=42)
        )
        response = client.get("/documents/training-samples")
        assert response.status_code == 200
        assert response.json()["trainable_samples_number"] == 42
        assert response.json()["institute_name"] == "TestInstitute"


class TestGetById:
    def test_returns_200_when_found(self, client, mock_service):
        mock_service.get_by_id = AsyncMock(return_value=_dto(id=5))
        response = client.get("/documents/5")
        assert response.status_code == 200
        assert response.json()["id"] == 5

    def test_returns_404_when_not_found(self, client, mock_service):
        mock_service.get_by_id = AsyncMock(side_effect=DocumentNotFoundError(document_id=5))
        assert client.get("/documents/5").status_code == 404

    def test_404_response_contains_document_id(self, client, mock_service):
        mock_service.get_by_id = AsyncMock(side_effect=DocumentNotFoundError(document_id=5))
        response = client.get("/documents/5")
        assert response.json()["document_id"] == 5


class TestUpdateDocumentTrainable:
    def test_returns_200_on_success(self, client, mock_service):
        mock_service.update_document_trainable = AsyncMock(return_value=_dto(id=1, is_trainable=True))
        response = client.put("/documents/trainability/1", json={"is_trainable": True})
        assert response.status_code == 200
        assert response.json()["is_trainable"] is True

    def test_returns_404_when_not_found(self, client, mock_service):
        mock_service.update_document_trainable = AsyncMock(
            side_effect=DocumentNotFoundError(document_id=1)
        )
        assert client.put("/documents/trainability/1", json={"is_trainable": True}).status_code == 404

    def test_missing_body_returns_422(self, client):
        assert client.put("/documents/trainability/1", json={}).status_code == 422


class TestUpdateDocumentExternallyApproved:
    def test_returns_200_on_success(self, client, mock_service):
        mock_service.update_document_externally_approved = AsyncMock(
            return_value=_dto(id=1, is_externally_approved=True)
        )
        response = client.put("/documents/externally-approved/1",
                               json={"is_externally_approved": True})
        assert response.status_code == 200
        assert response.json()["is_externally_approved"] is True

    def test_returns_404_when_not_found(self, client, mock_service):
        mock_service.update_document_externally_approved = AsyncMock(
            side_effect=DocumentNotFoundError(document_id=1)
        )
        assert client.put("/documents/externally-approved/1",
                          json={"is_externally_approved": True}).status_code == 404

    def test_missing_body_returns_422(self, client):
        assert client.put("/documents/externally-approved/1", json={}).status_code == 422


class TestDeleteById:
    def test_returns_204(self, client, mock_service):
        mock_service.delete_by_id = AsyncMock(return_value=None)
        assert client.delete("/documents/1").status_code == 204

    def test_returns_404_when_not_found(self, client, mock_service):
        mock_service.delete_by_id = AsyncMock(side_effect=DocumentNotFoundError(document_id=1))
        assert client.delete("/documents/1").status_code == 404
