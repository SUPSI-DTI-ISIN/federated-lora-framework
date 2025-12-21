from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from commons import Environment

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    database_url: str
    cors_origins: List[str] = ["http://localhost:3000"]
    environment: str = Environment.DEV

    @field_validator("cors_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v