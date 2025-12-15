import argparse
import os.path

from typing import List

from domain.document import Document
from domain.training import TrainingDataset
from utils import settings
from services.parser import PdfParserFacade
from services.dataset import DatasetService
from training import train


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--folder", help="Pdf Folder path", default="./pdf-innosuisse", type=str)

    return parser.parse_args()

def core(pdf_folder: str):
    documents: List[Document] = PdfParserFacade.parse_pdf_files(pdf_folder=pdf_folder)

    dataset: TrainingDataset = DatasetService.build_dataset_from_documents(documents=documents)
    os.makedirs(settings.dataset_output_path, exist_ok=True)
    dataset.to_jsonl(output_path=settings.dataset_output_path)

    print("train...")
    #train(dataset_file)


if __name__ == '__main__':
    args = parse_arguments()
    core(pdf_folder=args.folder)