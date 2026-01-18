from pydantic_settings import BaseSettings, SettingsConfigDict

from commons import Environment

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    model_key: str

    mlflow_tracking_uri: str
    mlflow_s3_endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str

    environment: str = Environment.DEV