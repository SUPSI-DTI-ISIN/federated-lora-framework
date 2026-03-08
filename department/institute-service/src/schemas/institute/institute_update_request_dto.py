from typing import Optional

from pydantic import BaseModel

class InstituteUpdateRequestDTO(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None