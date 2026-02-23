from typing import Optional

from pydantic import BaseModel

class InstituteCreationRequestDTO(BaseModel):
    name: str
    url: str
    deletable: Optional[bool] = True