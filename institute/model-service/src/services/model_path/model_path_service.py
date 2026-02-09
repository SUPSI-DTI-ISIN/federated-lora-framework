import os
from pathlib import Path
from typing import Optional

from commons import ModelPathUtils
from schemas.model import ModelPathDTO
from .model_path_service_interface import ModelPathServiceInterface


class ModelPathService(ModelPathServiceInterface):
    __INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE


    def get_model_path(self, model_key: str, adapter_version: Optional[int]) -> ModelPathDTO:
        model_base_path = ModelPathUtils.get_model_base_path(model_key=model_key)
        adapter_path = ModelPathUtils.get_model_adapter_path_by_version(model_key=model_key, version=adapter_version) if adapter_version is not None else adapter_version

        if not os.path.exists(model_base_path):
            raise FileNotFoundError(f"Model path does not exist model {model_key}")

        if adapter_path is None:
            return ModelPathDTO(
                model_base_path=str(Path(model_base_path).resolve())
            )

        if not os.path.exists(adapter_path):
            raise FileNotFoundError(f"Adapter with version {adapter_version} for model {model_key} does not exist")

        return ModelPathDTO(
            model_base_path=str(Path(model_base_path).resolve()),
            adapter_path=str(Path(adapter_path).resolve())
        )
