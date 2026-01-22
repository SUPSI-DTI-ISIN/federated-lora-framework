from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

from commons import Environment

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    model_id: str
    frontend_url: str = "http://localhost:3000"
    model_service_url: str = "http://localhost:8090"
    environment: str = Environment.DEV

    @property
    def cors_origins(self) -> List[str]:
        return [self.frontend_url]