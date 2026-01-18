from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

from commons import Environment

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    model_key: str
    frontend_url: str = "http://localhost:3000"
    mlflow_service_url: str = "http://localhost:9010"
    environment: str = Environment.DEV

    @property
    def cors_origins(self) -> List[str]:
        return [self.frontend_url]