from pathlib import Path
from app.config.settings import settings
from app.parser.pymupdf_parser import PyMuPdfParser

class PdfReader:
    def __init__(self) -> None:
        self.pdf_foldername: str = settings.pdf_folder
        self.pdf_parser: PyMuPdfParser = PyMuPdfParser()
    
    def parse_pdf(self):
        print(f"Start parsing pdf files from folder {self.pdf_foldername}")
        pdf_folder = Path(self.pdf_foldername)

        if not pdf_folder.exists():
            print("Folder does not exist")
            return
        
        for pdf_file in pdf_folder.glob("*.pdf"):
            try:
                self.pdf_parser.load(str(pdf_file))
                print(f"Parsing pdf: {str(pdf_file.absolute())}")
                print(f"Number of pages: {self.pdf_parser.get_pages()}")
            finally:
                self.pdf_parser.close()
