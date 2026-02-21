from pydantic import BaseModel

class InstituteCreationRequestDTO(BaseModel):
    name: str
    url: str