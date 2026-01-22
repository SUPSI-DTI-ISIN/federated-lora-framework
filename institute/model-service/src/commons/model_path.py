import os

from config import settings


class ModelPath:
    MODEL_BASE_PATH = settings.model_base_path

    @classmethod
    def get_model_base_path(cls) -> str:
        return os.path.join(cls.MODEL_BASE_PATH, "base")

    @classmethod
    def get_model_adapter_path_by_version(cls, version: int) -> str:
        return os.path.join(cls.MODEL_BASE_PATH, "adapters", str(version))