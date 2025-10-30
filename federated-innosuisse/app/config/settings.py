import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pdf_folder: str = "./pdf-innosuisse"
    model_folder: str = "./models/llama-2-7b"
    output_folder: str = "./output"

settings = Settings()
