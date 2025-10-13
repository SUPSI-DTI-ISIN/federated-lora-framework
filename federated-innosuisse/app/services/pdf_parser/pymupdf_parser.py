import pymupdf

from pathlib import Path
from typing import List
from pymupdf import Page
from typing_extensions import override
from app.services.pdf_parser.base_pdf_parser import BasePdfParser


class PyMuPdfParser(BasePdfParser):
    def __init__(self) -> None:
        self.document = None

    @override
    def load(self, filename: Path) -> None:
        self.document = pymupdf.open(filename)
        if not self.document.is_pdf:
            raise Exception("File passed is not a pdf")

    @override
    def get_all_text_document(self) -> str:
        if not self._is_document_open():
            raise Exception("Document is not open")
        
        text_per_page: List[str] = []
        
        for page in self.get_pages():
            text_per_page.append(page.get_textpage().extractText())
        
        return "\n".join(text_per_page)
    
    @override
    def get_pages(self) -> List[Page]:
        if not self._is_document_open():
            raise Exception("Document is not open")

        return self.document

    @override
    def close(self) -> None:
        if self._is_document_open():
            self.document.close()
            self.document = None

    def _is_document_open(self) -> bool:
        return self.document is not None and not self.document.is_closed