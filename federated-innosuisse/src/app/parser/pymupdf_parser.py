import fitz

from typing_extensions import override
from app.parser.base_parser import BaseParser


class PyMuPdfParser(BaseParser):
    def __init__(self) -> None:
        self.document = None
        self.filename = None

    @override
    def load(self, filename: str) -> bool:
        try:
            self.filename = filename
            self.document = fitz.open(filename)
            if not self.document.is_pdf:
                print("File passed is not a pdf")
                return False
            return True    
        except Exception:
            print("Error loading file")
            return False


    def get_pages(self) -> int:
        return self.document.page_count

    @override
    def close(self) -> None:
        if(self.document):
            self.document.close()
            self.document = None