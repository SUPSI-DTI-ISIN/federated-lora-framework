from dataclasses import dataclass

from peft import PeftModel
from transformers import AutoTokenizer


@dataclass
class LlmModel:
    model: PeftModel
    tokenizer: AutoTokenizer