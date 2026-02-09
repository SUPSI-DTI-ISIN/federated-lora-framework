import os

from federated_learning_client.config import settings

class FileUtils:
    @staticmethod
    def get_dataset_output_file(partition_id: int) -> str:
        partition_folder = os.path.join(settings.dataset_output_folder, str(partition_id))
        os.makedirs(partition_folder, exist_ok=True)
        return os.path.join(partition_folder, "dataset.jsonl")

    @staticmethod
    def get_training_folder(partition_id: int) -> str:
        training_folder = os.path.join(settings.dataset_output_folder, str(partition_id), "training")
        os.makedirs(training_folder, exist_ok=True)
        return training_folder