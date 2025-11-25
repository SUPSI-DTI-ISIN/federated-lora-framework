from pathlib import Path
from typing import List

from app import commons
from app.domain import Document
from app.parser.pdf_parser import PdfParser


def parse_pdf_files(pdf_folder: str) -> List[Document]:
    pdf_folder = Path(pdf_folder)

    if not commons.is_folder_valid(pdf_folder):
        return []

    documents: List[Document] = []
    for pdf_file in commons.get_pdf_files_from_folder(pdf_folder):
        with PdfParser(pdf_file) as pdf_parser:
            documents.append(
                Document(
                    metadata=pdf_parser.get_metadata(),
                    sections=pdf_parser.get_sections()
                )
            )
        del pdf_parser
    return documents