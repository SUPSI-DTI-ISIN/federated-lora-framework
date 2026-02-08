from typing import Optional
from pydantic import BaseModel


class ChatDTO(BaseModel):
    id: int
    user_id: str
    title: Optional[str]