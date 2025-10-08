import json
from pymupdf import Page
from pathlib import Path
from typing import List
from app.config.settings import settings
from app.parser.pymupdf_parser import PyMuPdfParser
from app.service.section.section_detector import SectionDetector

class PdfReader:
    def __init__(self) -> None:
        self.pdf_foldername: str = settings.pdf_folder
        self._pdf_parser: PyMuPdfParser = PyMuPdfParser()
        self._section_detector: SectionDetector = SectionDetector()
        self._batch_size = 3
    
    def parse_pdf(self):
        print(f"Start parsing pdf files from folder {self.pdf_foldername}")
        pdf_folder = Path(self.pdf_foldername)

        if not pdf_folder.exists():
            print("Folder does not exist")
            return
        
        pdf_file_list = list(pdf_folder.glob("*.pdf"))
        
        for pdf_file in pdf_file_list:
            try:
                self._pdf_parser.load(str(pdf_file))
                
                text_document = self._pdf_parser.get_text_document()

                pages = self._pdf_parser.get_pages()
                buffer: List[str] = []

                for page in pages:
                    page_text = page.get_textpage().extractText()

                    buffer.append(page_text)

                    if len(buffer) == self._batch_size:
                        joined_text = "\n".join(buffer)
                        sections = self._section_detector.detect_sections(joined_text)
                        buffer = []

                if buffer:
                    joined_text = "\n".join(buffer)
                    sections = self._section_detector.detect_sections(joined_text)

            finally:
                self._pdf_parser.close()
