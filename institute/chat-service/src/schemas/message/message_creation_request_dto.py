from typing import Optional

from pydantic import BaseModel

from entities import MessageRole


class MessageCreationRequestDTO(BaseModel):
    chat_id: int
    role: MessageRole
    content: str
    model_key: str
    adapter_version: Optional[int]