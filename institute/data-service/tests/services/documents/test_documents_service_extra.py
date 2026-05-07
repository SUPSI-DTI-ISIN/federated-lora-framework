import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from schemas.exceptions import InvalidFileError
from services.documents.documents_service import DocumentsService


@pytest.fixture()
def repo():
    return AsyncMock()


@pytest.fixture()
def service(repo):
    return DocumentsService(documents_repository=repo, institute_name="TestInstitute")


class TestUploadDataEdgeCases:
    async def test_raises_invalid_file_when_parsed_document_is_none(self, service, repo):
        repo.get_by_number = AsyncMock(return_value=None)

        mock_parser = MagicMock()
        mock_parser.__enter__ = MagicMock(return_value=mock_parser)
        mock_parser.__exit__ = MagicMock(return_value=False)
        mock_parser.get_document = MagicMock(return_value=None)

        mock_tmp_file = MagicMock()
        mock_tmp_file.__enter__ = MagicMock(return_value=mock_tmp_file)
        mock_tmp_file.__exit__ = MagicMock(return_value=False)
        mock_tmp_file.name = "/tmp/test.pdf"

        mock_path = MagicMock()
        mock_path.exists.return_value = True

        with patch("services.documents.documents_service.PdfParserService", return_value=mock_parser), \
             patch("services.documents.documents_service.tempfile.NamedTemporaryFile",
                   return_value=mock_tmp_file), \
             patch("services.documents.documents_service.os.remove"), \
             patch("services.documents.documents_service.Path", return_value=mock_path):
            with pytest.raises(InvalidFileError, match="Invalid document data"):
                await service.upload_data(file_content=b"PDF content", is_externally_approved=False)
