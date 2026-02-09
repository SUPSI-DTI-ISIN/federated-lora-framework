import pymupdf

from pathlib import Path
from typing import List
from pymupdf import Page

from commons.documents import ParsedDocument
from .extractor import SectionExtractor, ProjectTitleExtractor, ProjectNumberExtractor


class PdfParserService:
    def __init__(self, pdf_file: Path) -> None:
        if not pdf_file or not pdf_file.is_file():
            raise Exception(f"PDF file '{pdf_file}' is not valid")

        self._document = None
        self._pdf_file = pdf_file
        self._open()

    def __enter__(self) -> "PdfParserService":
        if not self._is_document_open():
            self._open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._close()
        return

    def get_document(self) -> ParsedDocument:
        return ParsedDocument(
            number=self._project_number,
            title=self._project_title,
            sections=SectionExtractor.extract_document_sections(text=self._full_text, project_number=self._project_number)
        )

    def _open(self) -> None:
        self._document = pymupdf.open(self._pdf_file)
        if not self._document.is_pdf:
            self._close()
            raise Exception("File passed is not a pdf")
        self._full_text = self._get_text_document()
        self._project_title = ProjectTitleExtractor.extract_project_title(text_document=self._full_text)
        self._project_number = ProjectNumberExtractor.extract_project_number(text_document=self._full_text)

    def _close(self) -> None:
        if self._is_document_open():
            self._document.close()
            self._document = None
            self._pdf_file = None

    def _is_document_open(self) -> bool:
        return self._document is not None and not self._document.is_closed

    def _get_text_document(self) -> str:
        text_per_page: List[str] = []

        for page in self._document:
            text_per_page.append(PdfParserService._get_text_from_page(page=page))

        return "\n".join(text_per_page)

    @staticmethod
    def _get_text_from_page(page: Page) -> str:
        return page.get_textpage().extractText()