import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from models import DocumentModel, SectionModel
from schemas.documents import DocumentDTO, TrainingSamplesDTO
from schemas.exceptions import DocumentNotFoundError, DocumentAlreadyExistsError, InvalidFileError
from services.documents.documents_service import DocumentsService


def _doc_model(id=1, number="DOC-001", title="Test Doc", is_trainable=False,
               is_externally_approved=False, sections=None):
    m = DocumentModel()
    m.id = id
    m.number = number
    m.title = title
    m.is_trainable = is_trainable
    m.is_externally_approved = is_externally_approved
    m.sections = sections or []
    return m


def _section_model(id=1, title="1. Intro", content="Content"):
    s = SectionModel()
    s.id = id
    s.document_id = 1
    s.title = title
    s.content = content
    return s


@pytest.fixture()
def repo():
    return AsyncMock()


@pytest.fixture()
def service(repo):
    return DocumentsService(documents_repository=repo, institute_name="TestInstitute")


def _patch_upload(mock_parsed, repo_get_by_number=None, repo_save=None):
    mock_parser = MagicMock()
    mock_parser.__enter__ = MagicMock(return_value=mock_parser)
    mock_parser.__exit__ = MagicMock(return_value=False)
    mock_parser.get_document = MagicMock(return_value=mock_parsed)

    mock_tmp_file = MagicMock()
    mock_tmp_file.__enter__ = MagicMock(return_value=mock_tmp_file)
    mock_tmp_file.__exit__ = MagicMock(return_value=False)
    mock_tmp_file.name = "/tmp/test.pdf"

    mock_path = MagicMock()
    mock_path.exists.return_value = True

    return mock_parser, mock_tmp_file, mock_path


class TestUploadData:
    async def test_raises_invalid_file_error_when_content_empty(self, service):
        with pytest.raises(InvalidFileError):
            await service.upload_data(file_content=b"", is_externally_approved=False)

    async def test_raises_invalid_file_error_when_content_is_none(self, service):
        with pytest.raises(InvalidFileError):
            await service.upload_data(file_content=None, is_externally_approved=False)

    async def test_raises_document_already_exists_when_duplicate(self, service, repo):
        existing = _doc_model(id=5)
        repo.get_by_number = AsyncMock(return_value=existing)

        mock_parsed = MagicMock()
        mock_parsed.number = "DOC-001"
        mock_parsed.title = "Test"
        mock_parsed.sections = []

        mock_parser, mock_tmp_file, mock_path = _patch_upload(mock_parsed)

        with patch("services.documents.documents_service.PdfParserService", return_value=mock_parser), \
             patch("services.documents.documents_service.tempfile.NamedTemporaryFile",
                   return_value=mock_tmp_file), \
             patch("services.documents.documents_service.os.remove"), \
             patch("services.documents.documents_service.Path", return_value=mock_path):
            with pytest.raises(DocumentAlreadyExistsError) as exc_info:
                await service.upload_data(file_content=b"PDF content", is_externally_approved=False)

        assert exc_info.value.document_id == 5

    async def test_saves_and_returns_dto_on_success(self, service, repo):
        repo.get_by_number = AsyncMock(return_value=None)
        saved = _doc_model(id=10, number="DOC-001")
        repo.save_document = AsyncMock(return_value=saved)

        mock_parsed = MagicMock()
        mock_parsed.number = "DOC-001"
        mock_parsed.title = "Test"
        mock_parsed.sections = []

        mock_parser, mock_tmp_file, mock_path = _patch_upload(mock_parsed)

        with patch("services.documents.documents_service.PdfParserService", return_value=mock_parser), \
             patch("services.documents.documents_service.DocumentMapper.to_model",
                   return_value=_doc_model()), \
             patch("services.documents.documents_service.tempfile.NamedTemporaryFile",
                   return_value=mock_tmp_file), \
             patch("services.documents.documents_service.os.remove"), \
             patch("services.documents.documents_service.Path", return_value=mock_path):
            dto = await service.upload_data(file_content=b"PDF content", is_externally_approved=True)

        assert isinstance(dto, DocumentDTO)
        assert dto.id == 10

    async def test_sets_is_externally_approved_on_model(self, service, repo):
        repo.get_by_number = AsyncMock(return_value=None)
        saved = _doc_model(id=1, is_externally_approved=True)
        repo.save_document = AsyncMock(return_value=saved)

        mock_parsed = MagicMock()
        mock_parsed.number = "DOC-001"
        mock_parsed.title = "Test"
        mock_parsed.sections = []

        doc_model_instance = _doc_model()
        mock_parser, mock_tmp_file, mock_path = _patch_upload(mock_parsed)

        with patch("services.documents.documents_service.PdfParserService", return_value=mock_parser), \
             patch("services.documents.documents_service.DocumentMapper.to_model",
                   return_value=doc_model_instance), \
             patch("services.documents.documents_service.tempfile.NamedTemporaryFile",
                   return_value=mock_tmp_file), \
             patch("services.documents.documents_service.os.remove"), \
             patch("services.documents.documents_service.Path", return_value=mock_path):
            await service.upload_data(file_content=b"PDF content", is_externally_approved=True)

        assert doc_model_instance.is_externally_approved is True

    async def test_cleans_up_temp_file_on_exception(self, service, repo):
        mock_parser = MagicMock()
        mock_parser.__enter__ = MagicMock(side_effect=Exception("parse error"))
        mock_parser.__exit__ = MagicMock(return_value=False)

        mock_tmp_file = MagicMock()
        mock_tmp_file.__enter__ = MagicMock(return_value=mock_tmp_file)
        mock_tmp_file.__exit__ = MagicMock(return_value=False)
        mock_tmp_file.name = "/tmp/test.pdf"

        mock_path = MagicMock()
        mock_path.exists.return_value = True

        with patch("services.documents.documents_service.PdfParserService", return_value=mock_parser), \
             patch("services.documents.documents_service.tempfile.NamedTemporaryFile",
                   return_value=mock_tmp_file), \
             patch("services.documents.documents_service.os.remove") as mock_remove, \
             patch("services.documents.documents_service.Path", return_value=mock_path):
            with pytest.raises(Exception):
                await service.upload_data(file_content=b"PDF content", is_externally_approved=False)

        mock_remove.assert_called_once()


class TestGetAll:
    async def test_returns_list_of_dtos(self, service, repo):
        repo.get_all = AsyncMock(return_value=[_doc_model(id=1), _doc_model(id=2)])

        result = await service.get_all()

        assert len(result) == 2
        assert all(isinstance(d, DocumentDTO) for d in result)

    async def test_returns_empty_list(self, service, repo):
        repo.get_all = AsyncMock(return_value=[])

        assert await service.get_all() == []


class TestGetAllTrainable:
    async def test_returns_trainable_dtos(self, service, repo):
        repo.get_all_trainable = AsyncMock(return_value=[_doc_model(id=1, is_trainable=True)])

        result = await service.get_all_trainable()

        assert len(result) == 1
        assert all(isinstance(d, DocumentDTO) for d in result)

    async def test_returns_empty_list(self, service, repo):
        repo.get_all_trainable = AsyncMock(return_value=[])

        assert await service.get_all_trainable() == []


class TestGetTrainingSamples:
    async def test_counts_sections_across_trainable_documents(self, service, repo):
        doc1 = _doc_model(id=1, sections=[_section_model(id=1), _section_model(id=2)])
        doc2 = _doc_model(id=2, sections=[_section_model(id=3)])
        repo.get_all_trainable = AsyncMock(return_value=[doc1, doc2])

        result = await service.get_training_samples()

        assert isinstance(result, TrainingSamplesDTO)
        assert result.trainable_samples_number == 3
        assert result.institute_name == "TestInstitute"

    async def test_returns_zero_when_no_trainable_documents(self, service, repo):
        repo.get_all_trainable = AsyncMock(return_value=[])

        result = await service.get_training_samples()

        assert result.trainable_samples_number == 0

    async def test_returns_zero_when_documents_have_no_sections(self, service, repo):
        repo.get_all_trainable = AsyncMock(return_value=[_doc_model(id=1, sections=[])])

        result = await service.get_training_samples()

        assert result.trainable_samples_number == 0


class TestGetById:
    async def test_returns_dto_when_found(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=_doc_model(id=5))

        dto = await service.get_by_id(document_id=5)

        assert isinstance(dto, DocumentDTO)
        assert dto.id == 5

    async def test_raises_not_found_when_missing(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(DocumentNotFoundError) as exc_info:
            await service.get_by_id(document_id=99)

        assert exc_info.value.document_id == 99


class TestUpdateDocumentTrainable:
    async def test_updates_and_returns_dto(self, service, repo):
        doc = _doc_model(id=1, is_trainable=False)
        updated = _doc_model(id=1, is_trainable=True)
        repo.get_by_id = AsyncMock(return_value=doc)
        repo.save_document = AsyncMock(return_value=updated)

        dto = await service.update_document_trainable(document_id=1, is_trainable=True)

        assert dto.is_trainable is True
        assert doc.is_trainable is True

    async def test_raises_not_found_when_missing(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(DocumentNotFoundError) as exc_info:
            await service.update_document_trainable(document_id=99, is_trainable=True)

        assert exc_info.value.document_id == 99


class TestUpdateDocumentExternallyApproved:
    async def test_updates_and_returns_dto(self, service, repo):
        doc = _doc_model(id=1, is_externally_approved=False)
        updated = _doc_model(id=1, is_externally_approved=True)
        repo.get_by_id = AsyncMock(return_value=doc)
        repo.save_document = AsyncMock(return_value=updated)

        dto = await service.update_document_externally_approved(
            document_id=1, is_externally_approved=True
        )

        assert dto.is_externally_approved is True
        assert doc.is_externally_approved is True

    async def test_raises_not_found_when_missing(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(DocumentNotFoundError) as exc_info:
            await service.update_document_externally_approved(
                document_id=99, is_externally_approved=True
            )

        assert exc_info.value.document_id == 99


class TestDeleteById:
    async def test_deletes_successfully(self, service, repo):
        doc = _doc_model(id=1)
        repo.get_by_id = AsyncMock(return_value=doc)

        await service.delete_by_id(document_id=1)

        repo.delete_document.assert_awaited_once_with(document_model=doc)

    async def test_raises_not_found_when_missing(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(DocumentNotFoundError) as exc_info:
            await service.delete_by_id(document_id=99)

        assert exc_info.value.document_id == 99
