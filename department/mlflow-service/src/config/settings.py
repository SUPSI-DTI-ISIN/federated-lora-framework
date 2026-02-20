from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    model_key: str
    keycloak_url: str
    realm_name: str

    model_base_path: str = "./model"
    frontend_url: str = "http://localhost:3001"
    keycloak_global_hostname_url: str = None

    # mlflow_tracking_uri: str
    # mlflow_s3_endpoint_url: str
    # aws_access_key_id: str
    # aws_secret_access_key: str

    @property
    def cors_origins(self) -> List[str]:
        return [self.frontend_url]