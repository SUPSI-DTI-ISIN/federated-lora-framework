from typing import Optional, List

from pydantic import BaseModel

from schemas.chat import ConversationDTO


class QueryRequestDTO(BaseModel):
    model_key: str
    adapter_version: Optional[int]
    prompt: str
    conversation_history: List[ConversationDTO]