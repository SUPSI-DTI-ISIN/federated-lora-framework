from typing import List
from peft import LoraConfig, TaskType

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    model_key: str
    keycloak_url: str
    realm_name: str

    device_map: str = "auto"
    model_base_path: str = "./model"
    frontend_url: str = "http://localhost:3001"
    keycloak_global_hostname_url: str = None

    rank: int = 8
    lora_alpha: int = 16
    lora_dropout: float = 0.05
    task_type: TaskType = TaskType.CAUSAL_LM

    @property
    def lora_config(self) -> LoraConfig:
        target_modules = [
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
        ]

        return LoraConfig(
            r=self.rank,
            lora_alpha=self.lora_alpha,
            target_modules=target_modules,
            lora_dropout=self.lora_dropout,
            task_type=self.task_type,
            bias="none"
        )

    @property
    def cors_origins(self) -> List[str]:
        return [self.frontend_url]