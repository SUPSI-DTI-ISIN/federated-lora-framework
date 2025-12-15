import argparse
import os.path

from typing import List

from domain.document import Document
from domain.training import TrainingDataset
from config import settings
from parser.core import parse_pdf_files
from dataset import build_dataset_from_documents
from training import train


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--folder", help="Pdf Folder path", default="./pdf-innosuisse", type=str)

    return parser.parse_args()

def core(pdf_folder: str):
    documents: List[Document] = parse_pdf_files(pdf_folder)

    dataset: TrainingDataset = build_dataset_from_documents(documents)

    dataset_file = os.path.join(settings.output_folder, "dataset.jsonl")
    os.makedirs(os.path.dirname(dataset_file), exist_ok=True)
    dataset.to_jsonl(dataset_file)

    print("train...")
    #train(dataset_file)


if __name__ == '__main__':
    args = parse_arguments()
    core(pdf_folder=args.folder)