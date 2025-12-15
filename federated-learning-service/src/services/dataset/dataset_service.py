from typing import List

from datasets import load_dataset, Split

from .dataset_utils import DatasetUtils
from domain.document import Document
from domain.training import TrainingRow, TrainingDataset

class DatasetService:
    @staticmethod
    def build_dataset_from_documents(documents: List[Document]):
        training_row_list: List[TrainingRow] = []

        for document in documents:
            for section in document.sections:
                example = DatasetUtils.create_training_row(
                    section=section,
                    metadata=document.metadata
                )
                training_row_list.append(example)

        return TrainingDataset(training_row_list)

    @staticmethod
    def load_data(dataset_path: str, test_size: float = 0.25):
        dataset = load_dataset("json", data_files={"train": dataset_path}, split=Split.TRAIN)

        dataset = dataset.train_test_split(test_size=test_size)
        train_dataset = dataset['train']
        eval_dataset = dataset['test']

        return train_dataset, eval_dataset