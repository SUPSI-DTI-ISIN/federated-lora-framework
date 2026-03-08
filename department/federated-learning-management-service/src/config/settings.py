from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    redis_url: str
    flwr_app_base_path: str
    federated_learning_deployment_environment: str = "local-simulation"

    keycloak_url: str
    realm_name: str
    keycloak_global_hostname_url: str = None

    is_federated_learning_simulation_environment: bool = False
    database_url: str = "mysql+aiomysql://root:root@localhost:33063/federated_learning_jobs"
    frontend_url: str = "http://localhost:3000"

    @property
    def cors_origins(self) -> List[str]:
        return [self.frontend_url]