from typing import Dict, List
from pymupdf import Page
from typing_extensions import override
from app.parser.base_parser import BaseParser


import pymupdf


class PyMuPdfParser(BaseParser):
    def __init__(self) -> None:
        self.document = None
        self.filename = None

    @override
    def load(self, filename: str) -> bool:
        try:
            self.filename = filename
            self.document = pymupdf.open(filename)
            if not self.document.is_pdf:
                print("File passed is not a pdf")
                return False
            return True    
        except Exception:
            print("Error loading file")
            return False


    @override
    def get_text_document(self) -> str:
        if not self._is_document_open():
            print("Document is not set or its already closed")
            return None
        
        text_per_page: List[str] = []
        
        for page in self.document:
            text_per_page.append(page.get_textpage().extractText())
        
        return "\n".join(text_per_page)
    
    @override
    def get_pages(self) -> List[Page]:
        if not self._is_document_open():
            print("Document is not set or its already closed")
            return None

        return self.document

    @override
    def close(self) -> None:
        if self._is_document_open():
            self.document.close()
            self.document = None

    def _is_document_open(self) -> bool:
        return self.document != None and not self.document.is_closed