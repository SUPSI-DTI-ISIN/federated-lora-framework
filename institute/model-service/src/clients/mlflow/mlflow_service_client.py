import requests
from pydantic import ValidationError

from clients.schemas import ManifestDTO, ModelAdaptersVersionDTO
from .mlflow_service_client_interface import MlFlowServiceClientInterface


class MlFlowServiceClient(MlFlowServiceClientInterface):
    __INSTANCE = None

    def __init__(self, department_service_url: str):
        self.__department_service_url = department_service_url

    @classmethod
    def get_instance(cls, department_service_url: str):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(department_service_url=department_service_url)
        return cls.__INSTANCE


    def get_model_base_manifest(self, model_key: str) -> ManifestDTO:
        model_base_manifest_url: str = f"{self.__department_service_url}/api_mlflow/model/{model_key}/manifest"
        try:
            resp = requests.get(model_base_manifest_url, headers={"Accept": "application/json"})
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

        data = resp.json()
        try:
            return ManifestDTO.model_validate(data)
        except ValidationError as e:
            raise RuntimeError(f"Invalid response shape: {e}")


    def get_model_file(self, model_key: str, model_file_path: str) -> requests.models.Response:
        file_url = f"{self.__department_service_url}/api_mlflow/model/{model_key}/file_name/{model_file_path}"
        try:
            resp = requests.get(file_url, stream=True)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

        return resp

    def get_adapters_version(self, model_key: str) -> ModelAdaptersVersionDTO:
        adapters_version_url: str = f"{self.__department_service_url}/api_mlflow/model/{model_key}/adapters"
        try:
            resp = requests.get(adapters_version_url, headers={"Accept": "application/json"})
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

        data = resp.json()
        try:
            return ModelAdaptersVersionDTO.model_validate(data)
        except ValidationError as e:
            raise RuntimeError(f"Invalid response shape: {e}")


    def get_adapter_manifest(self, model_key: str, adapter_version: int) -> ManifestDTO:
        adapter_manifest_url: str = f"{self.__department_service_url}/api_mlflow/model/{model_key}/adapters/{adapter_version}/manifest"
        try:
            resp = requests.get(adapter_manifest_url, headers={"Accept": "application/json"})
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

        data = resp.json()
        try:
            return ManifestDTO.model_validate(data)
        except ValidationError as e:
            raise RuntimeError(f"Invalid response shape: {e}")


    def get_adapter_file(self, model_key: str, adapter_version: int, model_file_path: str) -> requests.models.Response:
        file_url = f"{self.__department_service_url}/api_mlflow/model/{model_key}/adapters/{adapter_version}/file_name/{model_file_path}"
        try:
            resp = requests.get(file_url, stream=True)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

        return resp