from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    redis_url: str
    flwr_app_path: str
    federated_learning_deployment_environment: str

    keycloak_url: str
    realm_name: str
    keycloak_global_hostname_url: str = None

    frontend_url: str = "http://localhost:3001"

    @property
    def cors_origins(self) -> List[str]:
        return [self.frontend_url]