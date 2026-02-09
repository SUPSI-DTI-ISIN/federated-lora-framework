from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MessageDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    chat_id: int
    role: str
    content: str
    model_key: str
    adapter_version: Optional[int]
    created_at: datetime