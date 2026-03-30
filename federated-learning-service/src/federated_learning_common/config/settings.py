from peft import LoraConfig, TaskType
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    rank: int = 4
    lora_alpha: int = 8
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