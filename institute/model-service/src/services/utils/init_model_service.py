import os.path
import requests

from commons import ModelPath

class InitModelService:
    _INSTANCE = None

    def __init__(self, department_nginx_service_url: str):
        self._department_nginx_service_url = department_nginx_service_url

    @classmethod
    def get_instance(cls, department_nginx_service_url: str):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls(department_nginx_service_url=department_nginx_service_url)
        return cls._INSTANCE


    def download_base_model(self) -> None:
        model_base_path = ModelPath.get_model_base_path()

        if self._is_model_base_already_exist(model_base_path=model_base_path):
            return None

        self._create_model_base_dir(model_base_path=model_base_path)

        base_model_url: str = f"{self._department_nginx_service_url}/api_mlflow/model/base"
        try:
            resp = requests.get(base_model_url, headers={"Accept": "application/json"})
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

        data = resp.json()
        print(data)

        return None


    def _is_model_base_already_exist(self, model_base_path) -> bool:
        return os.path.exists(model_base_path) and os.path.isdir(model_base_path) and os.listdir(model_base_path)

    def _create_model_base_dir(self, model_base_path) -> None:
        os.makedirs(model_base_path, exist_ok=True)