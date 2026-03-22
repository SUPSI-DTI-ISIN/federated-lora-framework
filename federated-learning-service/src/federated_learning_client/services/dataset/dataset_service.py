import json

from dataclasses import asdict
from typing import List, Optional
from datasets import load_dataset, Split

from .dataset_utils import DatasetUtils

from src.federated_learning_client.clients.schemas import DocumentDTO
from src.federated_learning_client.domain.training import TrainingDataset
from src.federated_learning_client.utils import FileUtils
from ...utils import Llama2Utils


class DatasetService:
    @staticmethod
    def build_dataset_from_documents(documents: List[DocumentDTO]) -> TrainingDataset:
        training_dataset = TrainingDataset(training_rows=[])

        for document in documents:
            document_training_rows = DatasetUtils.create_document_training_rows(document=document)
            training_dataset.training_rows.extend(document_training_rows)

        return training_dataset

    @staticmethod
    def save_dataset_to_jsonl(training_dataset: TrainingDataset, partition_id: Optional[int] = None):
        dataset_output_file = FileUtils.get_dataset_output_file(partition_id=partition_id)
        with open(dataset_output_file, 'w', encoding='utf-8') as output:
            for training_row in training_dataset.training_rows:
                formatted_training_row = Llama2Utils.format_llama2_chat(
                    system=training_row.instruction,
                    user=training_row.input,
                    assistant=training_row.output
                )
                training_row_record = asdict(training_row)
                training_row_record.update(formatted_training_row)
                output.write(json.dumps(training_row_record, ensure_ascii=False) + '\n')

    @staticmethod
    def load_data(test_size: float = 0.25, partition_id: Optional[int] = None):
        dataset_file_path = FileUtils.get_dataset_output_file(partition_id=partition_id)

        dataset = load_dataset("json", data_files={"train": dataset_file_path}, split=Split.TRAIN)

        dataset = dataset.train_test_split(test_size=test_size)
        train_dataset = dataset['train']
        eval_dataset = dataset['test']

        return train_dataset, eval_dataset