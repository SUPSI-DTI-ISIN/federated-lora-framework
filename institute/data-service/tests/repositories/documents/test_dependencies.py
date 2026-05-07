from unittest.mock import AsyncMock

from repositories.documents.dependencies import get_documents_repository
from repositories.documents.documents_repository import DocumentsRepository


class TestGetDocumentsRepository:
    def test_returns_documents_repository_instance(self):
        mock_session = AsyncMock()
        repo = get_documents_repository(db=mock_session)
        assert isinstance(repo, DocumentsRepository)
