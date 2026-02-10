from peft import LoraConfig, TaskType
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    rank: int = 8
    lora_alpha: int = 16
    lora_dropout: float = 0.05
    task_type: TaskType = TaskType.CAUSAL_LM

    @property
    def lora_config(self) -> LoraConfig:
        target_modules = [
            "q_proj",    # Query projection in attention
            "k_proj",    # Key projection in attention
            "v_proj",    # Value projection in attention
            "o_proj",    # Output projection in attention
            "gate_proj", # Gate projection in MLP (for Llama-style)
            "up_proj",   # Up projection in MLP
            "down_proj", # Down projection in MLP
        ]

        return LoraConfig(
            r=self.rank,
            lora_alpha=self.lora_alpha,
            target_modules=target_modules,
            lora_dropout=self.lora_dropout,
            task_type=self.task_type,
            bias="none"
        )