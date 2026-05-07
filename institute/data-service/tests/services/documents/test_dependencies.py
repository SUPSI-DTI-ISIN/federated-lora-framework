from unittest.mock import AsyncMock

from services.documents.dependencies import get_documents_service
from services.documents.documents_service import DocumentsService


class TestGetDocumentsService:
    def test_returns_documents_service_instance(self):
        mock_repo = AsyncMock()
        service = get_documents_service(documents_repository=mock_repo)
        assert isinstance(service, DocumentsService)
