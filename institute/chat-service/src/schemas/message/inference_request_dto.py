from typing import Optional

from pydantic import BaseModel

class InferenceRequestDTO(BaseModel):
    model_key: str
    adapter_version: Optional[int]
    prompt: str