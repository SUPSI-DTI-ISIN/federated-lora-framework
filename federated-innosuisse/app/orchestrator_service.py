import json
import app.commons as commons

from pathlib import Path
from typing import List

from app.domain import Document
from app.services.pdf_parser import PdfParser

def _parse_pdf_files(pdf_folder: Path) -> List[Document]:
    documents: List[Document] = []
    for pdf_file in commons.get_pdf_files_from_folder(pdf_folder):
        with PdfParser(pdf_file) as pdf_parser:
            documents.append(
                Document(
                    metadata=pdf_parser.get_metadata(),
                    sections=pdf_parser.get_sections()
                )
            )
    return documents


def core(pdf_folder: str):
    pdf_folder = Path(pdf_folder)

    if not commons.is_folder_valid(pdf_folder):
        exit(1)

    documents: List[Document] = _parse_pdf_files(pdf_folder)

    for document in documents:
        print(json.dumps(document.to_json(), indent=4))