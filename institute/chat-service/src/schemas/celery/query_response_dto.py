from typing import Optional

from pydantic import BaseModel

class QueryResponseDTO(BaseModel):
    user_id: str
    chat_id: int
    prompt: str
    response: str
    model_key: str
    adapter_version: Optional[int]