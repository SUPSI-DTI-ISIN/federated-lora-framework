import os.path

import app.dataset as dataset_builder
import app.commons as commons
import app.training as trainer

from pathlib import Path
from typing import List

from app.domain import Document, TrainingDataset
from app.services.pdf_parser import PdfParser
from app.config.settings import settings


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

    dataset: TrainingDataset = dataset_builder.build_dataset_from_documents(documents)

    dataset_file = os.path.join(settings.output_folder, "dataset.jsonl")
    os.makedirs(os.path.dirname(dataset_file), exist_ok=True)
    dataset.to_jsonl(dataset_file)

    trainer.train()