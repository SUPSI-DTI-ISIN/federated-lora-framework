from typing import Optional

from pydantic import BaseModel

class QueryResponseDTO(BaseModel):
    prompt: str
    response: str
    model_key: str
    adapter_version: Optional[int]