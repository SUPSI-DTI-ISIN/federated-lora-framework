from pydantic import BaseModel

class QueryRequestDTO(BaseModel):
    prompt: str