from typing import List

from pydantic import BaseModel

from .model_file_dto import ModelFileDTO


class ModelManifestDTO(BaseModel):
    model_key: str
    files: List[ModelFileDTO] = []