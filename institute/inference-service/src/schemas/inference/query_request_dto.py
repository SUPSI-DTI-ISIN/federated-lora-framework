from typing import Optional, List

from pydantic import BaseModel

from schemas.inference import ConversationDTO


class QueryRequestDTO(BaseModel):
    user_id: str
    chat_id: int
    model_key: str
    adapter_version: Optional[int]
    prompt: str
    conversation_history: List[ConversationDTO]