from pydantic import BaseModel


class ConversationDTO(BaseModel):
    role: str
    content: str