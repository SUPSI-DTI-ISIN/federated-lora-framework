from pathlib import Path
from typing import List

from domain.document import Document
from utils import FileUtils
from .pdf_parser_service import PdfParserService

class PdfParserFacade:
    _PDF_FILES_PATTERN: str = "*.pdf"

    @classmethod
    def parse_pdf_files(cls, pdf_folder: str) -> List[Document]:
        pdf_folder = Path(pdf_folder)

        if not FileUtils.is_folder_valid(pdf_folder):
            return []

        documents: List[Document] = []
        for pdf_file in FileUtils.get_files_from_folder(pdf_folder, cls._PDF_FILES_PATTERN):
            with PdfParserService(pdf_file) as pdf_parser:
                documents.append(
                    Document(
                        metadata=pdf_parser.get_metadata(),
                        sections=pdf_parser.get_sections()
                    )
                )
        return documents