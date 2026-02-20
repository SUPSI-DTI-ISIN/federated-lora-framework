from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    keycloak_url: str
    institute_name: str
    model_key: str
    keycloak_global_hostname_url: str = None

    model_base_path: str = "./model"
    frontend_url: str = "http://localhost:3000"
    mlflow_department_service_url: str = "http://localhost:9010/api_mlflow"

    @property
    def cors_origins(self) -> List[str]:
        return [self.frontend_url]