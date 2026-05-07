from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelCacheKey:
    model_key: str
    adapter_version: Optional[str]

    def __hash__(self):
        return hash((self.model_key, self.adapter_version))

    def __eq__(self, other):
        return self.model_key == other.model_key and self.adapter_version == other.adapter_version