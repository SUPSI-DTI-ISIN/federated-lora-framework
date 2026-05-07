from pathlib import Path
from typing import List

from .file_hash_utils import FileHashUtils
from schemas.model import ManifestDTO, FileDTO


class ManifestUtils:
    @classmethod
    def get_manifest(cls, base_path: Path, model_key: str) -> ManifestDTO:
        files: List[FileDTO] = []

        for file_path in Path(base_path).rglob('*'):
            if file_path.is_file():
                rel_path = str(file_path.relative_to(base_path))
                model_file_dto = FileDTO(
                    rel_path=rel_path,
                    size=file_path.stat().st_size,
                    hash=FileHashUtils.get_file_hash(file_path=file_path)
                )
                files.append(model_file_dto)

        return ManifestDTO(
            model_key=model_key,
            files=files
        )