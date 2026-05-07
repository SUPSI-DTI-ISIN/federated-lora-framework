import pytest
from unittest.mock import MagicMock, patch


class TestPdfParserServiceClose:
    def test_close_does_nothing_when_already_closed(self, tmp_path):
        """Covers the _close branch when _is_document_open() is False (line 46->exit)."""
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
        parser._close()
        assert parser._document is None
