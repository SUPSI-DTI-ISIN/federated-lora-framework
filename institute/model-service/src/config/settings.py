from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

from commons import Environment

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    model_key: str
    frontend_url: str = "http://localhost:3000"
    department_service_url: str = "http://localhost:81"
    environment: str = Environment.DEV
    model_base_path: str = "./model"

    @property
    def cors_origins(self) -> List[str]:
        return [self.frontend_url]