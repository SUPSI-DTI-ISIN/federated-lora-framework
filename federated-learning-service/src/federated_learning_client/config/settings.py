from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    # Actually it takes this value from .toml value inside federated-learning-service (where simulation start and there is main .toml for FL service)
    data_service_url: str = "http://localhost:8080"
    model_service_url: str = "http://localhost:8090"
    device_map: str = "auto"
    model_key: str = "llama-2-7b"
    dataset_output_folder: str = "./output"