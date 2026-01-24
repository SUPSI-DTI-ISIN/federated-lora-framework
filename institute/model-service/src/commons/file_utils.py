import os
from pathlib import Path
from typing import List

from clients.schemas import ManifestDTO
from .file_hash_utils import FileHashUtils


class FileUtils:
    @classmethod
    def check_local_files_validity(cls, target_folder_path: Path, manifest: ManifestDTO) -> List[str]:
        print("Checking local model validity...")
        model_name = manifest.model_key

        invalid_or_missing_files = []

        for model_file_item in manifest.files:
            model_file_path = os.path.join(target_folder_path, model_file_item.rel_path)
            if not os.path.exists(model_file_path):
                print(f"- missing model file: {model_file_path}")
                invalid_or_missing_files.append(model_file_item.rel_path)
                continue
            if FileHashUtils.get_file_hash(file_path=Path(model_file_path)) != model_file_item.hash:
                print(f"- corrupted model file: {model_file_path}")
                invalid_or_missing_files.append(model_file_item.rel_path)
                continue
            else:
                print(f"- model file: {model_file_path} is valid.")

        if not invalid_or_missing_files:
            print(f"Model {model_name} is valid locally.")

        return invalid_or_missing_files

    @classmethod
    def delete_files(cls, target_folder_path: Path, model_files: List[str]) -> None:
        for model_file in model_files:
            model_file_path = os.path.join(target_folder_path, model_file)
            if os.path.exists(model_file_path):
                os.remove(model_file_path)
                print(f"Deleted model file {model_file_path}")