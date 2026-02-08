from typing import Optional

from pydantic import BaseModel


class ChatCreationRequestDTO(BaseModel):
    title: Optional[str] = None