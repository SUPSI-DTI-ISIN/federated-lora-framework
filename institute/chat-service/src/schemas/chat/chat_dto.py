from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ChatDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: str
    title: Optional[str]
    is_doing_inference: bool
    created_at: datetime
    updated_at: datetime