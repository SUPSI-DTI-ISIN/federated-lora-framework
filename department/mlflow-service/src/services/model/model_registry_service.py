from pathlib import Path
from typing import List

from commons import ModelPathUtils, FileHashUtils, ManifestUtils, FileUtils
from schemas.model import ManifestDTO, FileDTO
from .model_registry_service_interface import ModelRegistryServiceInterface


class ModelRegistryService(ModelRegistryServiceInterface):
    __INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE

    def get_model_manifest(self, model_key: str) -> ManifestDTO:
        model_base_path = ModelPathUtils.get_model_base_path(model_key=model_key)

        if not Path(model_base_path).exists():
            raise FileNotFoundError(f"Model with {model_key} does not exist")

        return ManifestUtils.get_manifest(base_path=Path(model_base_path), model_key=model_key)


    def get_model_file(self, model_key: str, file_name: str) -> Path:
        model_base_path = ModelPathUtils.get_model_base_path(model_key=model_key)

        if not Path(model_base_path).exists():
            raise FileNotFoundError(f"Model with {model_key} does not exist")

        return FileUtils.join_paths(base_path=Path(model_base_path), file_name=file_name)

    def get_model_path(self, model_key: str) -> str:
        model_base_path = Path(ModelPathUtils.get_model_base_path(model_key=model_key))

        if not model_base_path.exists():
            raise FileNotFoundError(f"Model with {model_key} does not exist")

        return str(model_base_path.resolve())