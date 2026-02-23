from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    keycloak_url: str
    institute_name: str
    keycloak_global_hostname_url: str = None

    database_url: str = "mysql+aiomysql://root:root@localhost:3306/documents"
    frontend_url: str = "http://localhost:3000"

    @property
    def cors_origins(self) -> List[str]:
        return [self.frontend_url]