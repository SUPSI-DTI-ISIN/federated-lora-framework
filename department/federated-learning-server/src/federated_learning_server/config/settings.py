from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    mlflow_service_url: str

    model_key: str = "llama-2-7b"
    device_map: str = "auto"