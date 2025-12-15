import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    pdf_folder: str = "./pdf-innosuisse"
    output_folder: str = "./output"

    dataset_file: str = "dataset.jsonl"
    dataset_path: str = os.path.join(output_folder, dataset_file)