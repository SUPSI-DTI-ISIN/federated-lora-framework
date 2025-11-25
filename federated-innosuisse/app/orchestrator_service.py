import os.path

from typing import List

from app.domain import Document, TrainingDataset
from app.config.settings import settings
from app.parser.core import parse_pdf_files
from app.dataset import build_dataset_from_documents
from app.training import train


def core(pdf_folder: str):
    documents: List[Document] = parse_pdf_files(pdf_folder)

    dataset: TrainingDataset = build_dataset_from_documents(documents)

    dataset_file = os.path.join(settings.output_folder, "dataset.jsonl")
    os.makedirs(os.path.dirname(dataset_file), exist_ok=True)
    dataset.to_jsonl(dataset_file)

    train(dataset_file)