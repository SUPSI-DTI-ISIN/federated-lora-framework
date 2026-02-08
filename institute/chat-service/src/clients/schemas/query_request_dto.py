from typing import Optional

from pydantic import BaseModel

class QueryRequestDTO(BaseModel):
    model_key: str
    adapter_version: Optional[int]
    prompt: str