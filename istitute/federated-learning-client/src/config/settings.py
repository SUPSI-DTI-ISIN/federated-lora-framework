from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    data_service_url: str = "cdsds"

    dataset_output_folder: str = "./output"