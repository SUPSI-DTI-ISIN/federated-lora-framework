from datetime import datetime
from dataclasses import dataclass

from transformers import PreTrainedModel, PreTrainedTokenizer


@dataclass
class LoadedModel:
    model: PreTrainedModel
    tokenizer: PreTrainedTokenizer
    has_adapter: bool
    loaded_at: datetime