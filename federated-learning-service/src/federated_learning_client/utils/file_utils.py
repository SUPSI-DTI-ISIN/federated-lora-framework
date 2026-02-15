import os

from typing import Optional

from src.federated_learning_client.config import settings

class FileUtils:
    @classmethod
    def get_dataset_output_file(cls, partition_id: Optional[int]) -> str:
        partition_folder = os.path.join(settings.dataset_output_folder, str(partition_id)) if partition_id is not None else settings.dataset_output_folder
        os.makedirs(partition_folder, exist_ok=True)
        return os.path.join(partition_folder, "dataset.jsonl")

    @classmethod
    def get_training_folder(cls, partition_id: Optional[int]) -> str:
        training_folder = os.path.join(settings.dataset_output_folder, str(partition_id), "training") if partition_id is not None else os.path.join(settings.dataset_output_folder, "training")
        os.makedirs(training_folder, exist_ok=True)
        return training_folder

    @classmethod
    def get_adapter_folder(cls, partition_id: Optional[int]) -> str:
        adapter_folder = os.path.join(settings.dataset_output_folder, str(partition_id), "adapter") if partition_id is not None else os.path.join(settings.dataset_output_folder, "adapter")
        os.makedirs(adapter_folder, exist_ok=True)
        return adapter_folder