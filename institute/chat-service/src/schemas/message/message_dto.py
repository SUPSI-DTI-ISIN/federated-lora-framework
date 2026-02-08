from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class MessageDTO(BaseModel):
    id: int
    chat_id: int
    role: str
    content: str
    model_key: str
    adapter_version: Optional[str]