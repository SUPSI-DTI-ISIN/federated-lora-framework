import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from tqdm import tqdm

from clients.mlflow import MlFlowServiceClientInterface
from clients.schemas import ManifestDTO
from commons import ModelPathUtils, FileHashUtils


class ModelValidityService:
    @classmethod
    def fetch_model(cls, mlflow_service_client: MlFlowServiceClientInterface, model_key: str, manifest: ManifestDTO, files_to_download = None) -> int:
        target_folder_path = ModelPathUtils.get_model_base_path(model_key=model_key)
        if not os.path.exists(target_folder_path):
            os.makedirs(target_folder_path)
        completed_transfers = 0

        model_files_to_download = manifest.files
        if files_to_download is not None:
            model_files_to_download = [
                file
                for file in manifest.files
                if file.rel_path in files_to_download
            ]

        with ThreadPoolExecutor(max_workers=20) as executor:

            futures = [
                executor.submit(cls.download_model_file, mlflow_service_client, model_key, model_file_item.rel_path,
                                model_file_item.hash, position)
                for position, model_file_item in enumerate(model_files_to_download)
            ]

            for future in as_completed(futures):
                success = future.result()
                if success:
                    completed_transfers += 1

        if completed_transfers != len(model_files_to_download):
            raise ValueError(f"The model {model_key} could not be found")

        return completed_transfers


    @classmethod
    def download_model_file(cls, mlflow_service_client: MlFlowServiceClientInterface, model_key: str, model_file_path: str, model_file_hash: str, position: int) -> bool:
        response = mlflow_service_client.get_model_file(model_key=model_key, model_file_path=model_file_path)

        total_size = int(response.headers.get('content-length', 0))
        chunk_size = 8192

        target_folder_path = ModelPathUtils.get_model_base_path(model_key=model_key)
        target_file_path = os.path.join(target_folder_path, model_file_path)
        bytes_written = 0

        with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Downloading {model_file_path}", position=position,
                  leave=True) as pbar:
            with open(target_file_path, 'wb') as f:

                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        bytes_written += len(chunk)
                        pbar.update(len(chunk))

        if FileHashUtils.get_file_hash(Path(target_file_path)) != model_file_hash:
            os.unlink(target_file_path)
            return False

        return True