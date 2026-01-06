import os

from client_app.config import settings

class FileUtils:
    @staticmethod
    def get_dataset_output_file() -> str:
        os.makedirs(settings.dataset_output_folder, exist_ok=True)
        return os.path.join(settings.dataset_output_folder, "dataset.jsonl")