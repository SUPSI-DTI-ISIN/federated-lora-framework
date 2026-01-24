from pydantic import BaseModel

class QueryRequestDTO(BaseModel):
    model_key: str
    adapter_version: int
    prompt: str