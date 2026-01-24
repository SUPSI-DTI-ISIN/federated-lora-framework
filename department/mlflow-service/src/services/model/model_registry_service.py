from pathlib import Path
from typing import List

from commons import ModelPathUtils, FileHashUtils
from schemas.model import ModelManifestDTO, ModelFileDTO
from .model_registry_service_interface import ModelRegistryServiceInterface


class ModelRegistryService(ModelRegistryServiceInterface):
    __INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE

    def get_model_manifest(self, model_key: str) -> ModelManifestDTO:
        model_base_path = ModelPathUtils.get_model_base_path(model_key=model_key)

        if not Path(model_base_path).exists():
            raise FileNotFoundError(f"Model with {model_key} does not exist")

        files: List[ModelFileDTO] = []

        for file_path in Path(model_base_path).rglob('*'):
            if file_path.is_file():
                rel_path = str(file_path.relative_to(model_base_path))
                model_file_dto = ModelFileDTO(
                    rel_path=rel_path,
                    size=file_path.stat().st_size,
                    hash=FileHashUtils.get_file_hash(file_path=file_path)
                )
                files.append(model_file_dto)

        return ModelManifestDTO(
            model_key=model_key,
            files=files
        )


    def get_model_file(self, model_key: str, file_name: str) -> Path:
        model_base_path = ModelPathUtils.get_model_base_path(model_key=model_key)

        if not Path(model_base_path).exists():
            raise FileNotFoundError(f"Model with {model_key} does not exist")

        file_path = Path(model_base_path).joinpath(file_name)
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_name} for Model with {model_key} is not existing")

        return file_path