import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock


class TestPdfParserServiceInit:
    def test_raises_when_file_is_none(self):
        from utils.pdf_parsing.pdf_parser_service import PdfParserService
        with pytest.raises(Exception):
            PdfParserService(pdf_file=None)

    def test_raises_when_file_does_not_exist(self, tmp_path):
        from utils.pdf_parsing.pdf_parser_service import PdfParserService
        non_existent = tmp_path / "missing.pdf"
        with pytest.raises(Exception):
            PdfParserService(pdf_file=non_existent)

    def test_raises_when_file_is_not_pdf(self, tmp_path):
        from utils.pdf_parsing.pdf_parser_service import PdfParserService
        txt_file = tmp_path / "test.txt"
        txt_file.write_bytes(b"not a pdf")

        mock_doc = MagicMock()
        mock_doc.is_pdf = False
        mock_doc.is_closed = False

        with patch("utils.pdf_parsing.pdf_parser_service.pymupdf.open", return_value=mock_doc):
            with pytest.raises(Exception, match="not a pdf"):
                PdfParserService(pdf_file=txt_file)

        mock_doc.close.assert_called_once()

    def test_opens_valid_pdf(self, tmp_path):
        from utils.pdf_parsing.pdf_parser_service import PdfParserService
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 fake")

        mock_page = MagicMock()
        mock_page.get_textpage.return_value.extractText.return_value = (
            "Number:\n DOC-001\nTitle:\n My Project\n1. Introduction\nContent\n"
        )

        mock_doc = MagicMock()
        mock_doc.is_pdf = True
        mock_doc.is_closed = False
        mock_doc.__iter__ = MagicMock(return_value=iter([mock_page]))

        with patch("utils.pdf_parsing.pdf_parser_service.pymupdf.open", return_value=mock_doc):
            parser = PdfParserService(pdf_file=pdf_file)

        assert parser is not None


class TestPdfParserServiceContextManager:
    def test_context_manager_opens_and_closes(self, tmp_path):
        from utils.pdf_parsing.pdf_parser_service import PdfParserService
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 fake")

        mock_page = MagicMock()
        mock_page.get_textpage.return_value.extractText.return_value = (
            "Number:\n DOC-001\nTitle:\n My Project\n1. Introduction\nContent\n"
        )

        mock_doc = MagicMock()
        mock_doc.is_pdf = True
        mock_doc.is_closed = False
        mock_doc.__iter__ = MagicMock(return_value=iter([mock_page]))

        with patch("utils.pdf_parsing.pdf_parser_service.pymupdf.open", return_value=mock_doc):
            with PdfParserService(pdf_file=pdf_file) as parser:
                assert parser is not None

        mock_doc.close.assert_called_once()

    def test_get_document_returns_parsed_document(self, tmp_path):
        from utils.pdf_parsing.pdf_parser_service import PdfParserService
        from commons.documents import ParsedDocument
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 fake")

        mock_page = MagicMock()
        mock_page.get_textpage.return_value.extractText.return_value = (
            "Number:\n DOC-001\nTitle:\n My Project\n1. Introduction\nContent here\n"
        )

        mock_doc = MagicMock()
        mock_doc.is_pdf = True
        mock_doc.is_closed = False
        mock_doc.__iter__ = MagicMock(return_value=iter([mock_page]))

        with patch("utils.pdf_parsing.pdf_parser_service.pymupdf.open", return_value=mock_doc):
            with PdfParserService(pdf_file=pdf_file) as parser:
                doc = parser.get_document()

        assert isinstance(doc, ParsedDocument)
        assert doc.number == "DOC-001"
        assert doc.title == "My Project"

    def test_enter_reopens_if_closed(self, tmp_path):
        from utils.pdf_parsing.pdf_parser_service import PdfParserService
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 fake")

        full_text = "Number:\n DOC-001\nTitle:\n My Project\n1. Introduction\nContent\n"

        mock_page = MagicMock()
        mock_page.get_textpage.return_value.extractText.return_value = full_text

        mock_doc = MagicMock()
        mock_doc.is_pdf = True
        mock_doc.is_closed = False
        mock_doc.__iter__ = MagicMock(return_value=iter([mock_page]))

        with patch("utils.pdf_parsing.pdf_parser_service.pymupdf.open", return_value=mock_doc):
            parser = PdfParserService(pdf_file=pdf_file)
            parser._document = None
            mock_page2 = MagicMock()
            mock_page2.get_textpage.return_value.extractText.return_value = full_text
            mock_doc2 = MagicMock()
            mock_doc2.is_pdf = True
            mock_doc2.is_closed = False
            mock_doc2.__iter__ = MagicMock(return_value=iter([mock_page2]))
            with patch("utils.pdf_parsing.pdf_parser_service.pymupdf.open", return_value=mock_doc2):
                result = parser.__enter__()
            assert result is parser
