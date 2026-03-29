from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    data_service_url: str = "http://localhost:8080"
    model_service_url: str = "http://localhost:8090"
    device_map: str = "auto"
    model_key: str = "llama-31-8b"
    dataset_output_folder: str = "./output"
    is_simulation_running_environment: bool = False