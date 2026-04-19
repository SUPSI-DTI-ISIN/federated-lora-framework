import os

from config import settings


class ModelPathUtils:
    MODEL_BASE_PATH = settings.model_base_path

    @classmethod
    def get_model_base_path(cls, model_key: str) -> str:
        return os.path.join(cls.MODEL_BASE_PATH, model_key, "base")

    @classmethod
    def get_model_adapters_path(cls, model_key: str) -> str:
        return os.path.join(cls.MODEL_BASE_PATH, model_key, "adapters")

    @classmethod
    def get_model_adapter_path_by_version(cls, model_key: str, version: int) -> str:
        return os.path.join(cls.MODEL_BASE_PATH, model_key, "adapters", str(version))

    @classmethod
    def get_model_init_adapter_path(cls, model_key: str) -> str:
        return os.path.join(cls.MODEL_BASE_PATH, model_key, "adapters", "init")