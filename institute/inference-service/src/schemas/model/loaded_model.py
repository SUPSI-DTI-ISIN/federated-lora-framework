from datetime import datetime
from dataclasses import dataclass
from typing import Union

from peft import PeftModel
from transformers import PreTrainedModel, PreTrainedTokenizer


@dataclass
class LoadedModel:
    model: Union[PreTrainedModel, PeftModel]
    tokenizer: PreTrainedTokenizer
    has_adapter: bool
    loaded_at: datetime