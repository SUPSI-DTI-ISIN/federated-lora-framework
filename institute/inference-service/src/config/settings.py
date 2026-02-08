from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    institute_name: str
    keycloak_url: str

    mock_llm_usage: bool = False

    max_cached_models: int = 2
    device_map: str = "auto"
    frontend_url: str = "http://localhost:3000"
    model_service_url: str = "http://localhost:8090"

    @property
    def cors_origins(self) -> List[str]:
        return [self.frontend_url]