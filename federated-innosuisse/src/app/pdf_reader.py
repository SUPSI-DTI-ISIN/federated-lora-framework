import json
from pymupdf import Page
from pathlib import Path
from typing import List
from app.config.settings import settings
from app.parser.pymupdf_parser import PyMuPdfParser
from app.service.project_number_detector.project_number_detector import ProjectNumberDetector
from app.service.section_detector.section_detector import SectionDetector
from app.service.text_cleaner.page_number_cleaner import PageNumberCleaner
from app.service.text_cleaner.telephone_number_cleaner import TelephoneNumberCleaner
from app.service.text_cleaner.text_cleaner import TextCleaner

class PdfReader:
    def __init__(self) -> None:
        self.pdf_foldername: str = settings.pdf_folder
        self._pdf_parser: PyMuPdfParser = PyMuPdfParser()
        self._text_cleaner: TextCleaner = TextCleaner([
            TelephoneNumberCleaner(),
            PageNumberCleaner()
        ])
        self._project_number_detector: ProjectNumberDetector = ProjectNumberDetector()
        self._section_detector: SectionDetector = SectionDetector()
        self._batch_size = 5
    
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

                pages = self._pdf_parser.get_pages()

                project_number = self._project_number_detector.extract_project_number(pages[0].get_textpage().extractText())
                print(f"project number is: {project_number}")

                full_text = self._pdf_parser.get_text_document()
                self._section_detector.detect_sections(full_text, project_number)
            finally:
                self._pdf_parser.close()
