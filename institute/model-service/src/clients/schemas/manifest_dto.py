from typing import List

from pydantic import BaseModel

from .file_dto import FileDTO


class ManifestDTO(BaseModel):
    model_key: str
    files: List[FileDTO] = []