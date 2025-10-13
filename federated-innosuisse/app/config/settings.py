import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pdf_folder: str = "./pdf-innosuisse"

settings = Settings()
