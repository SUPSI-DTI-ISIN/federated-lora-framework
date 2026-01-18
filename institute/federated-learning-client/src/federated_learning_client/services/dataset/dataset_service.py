import json

from dataclasses import asdict
from typing import List
from datasets import load_dataset, Split

from .dataset_utils import DatasetUtils
from federated_learning_client.domain.document import DocumentDTO
from federated_learning_client.domain.training import TrainingDataset
from federated_learning_client.utils import FileUtils


class DatasetService:
    @staticmethod
    def build_dataset_from_documents(documents: List[DocumentDTO]) -> TrainingDataset:
        training_dataset = TrainingDataset(training_rows=[])

        for document in documents:
            document_training_rows = DatasetUtils.create_document_training_rows(document=document)
            training_dataset.training_rows.extend(document_training_rows)

        return training_dataset

    @staticmethod
    def save_dataset_to_jsonl(training_dataset: TrainingDataset, dataset_output_file: str = FileUtils.get_dataset_output_file()):
        with open(dataset_output_file, 'w', encoding='utf-8') as output:
            for training_row in training_dataset.training_rows:
                output.write(json.dumps(asdict(training_row), ensure_ascii=False) + '\n')

    @staticmethod
    def load_data(dataset_file_path: str = FileUtils.get_dataset_output_file(), test_size: float = 0.25):
        dataset = load_dataset("json", data_files={"train": dataset_file_path}, split=Split.TRAIN)

        dataset = dataset.train_test_split(test_size=test_size)
        train_dataset = dataset['train']
        eval_dataset = dataset['test']

        return train_dataset, eval_dataset