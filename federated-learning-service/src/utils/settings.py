import os

from peft import LoraConfig
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    device: str = "auto"

    rank: int = 8
    lora_alpha: int = 16
    lora_dropout: float = 0.05
    task_type: str = "CAUSAL_LM"

    pdf_folder: str = "./pdf-innosuisse"
    output_folder: str = "./output"

    @property
    def lora_config(self) -> LoraConfig:
        return LoraConfig(
            r=self.rank,
            lora_alpha=self.lora_alpha,
            lora_dropout=self.lora_dropout,
            task_type=self.task_type,
        )

    @property
    def dataset_output_path(self) -> str:
        return os.path.join(self.output_folder, "dataset.jsonl")