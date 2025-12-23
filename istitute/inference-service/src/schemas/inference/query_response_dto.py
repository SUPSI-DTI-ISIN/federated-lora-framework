from pydantic import BaseModel

class QueryResponseDTO(BaseModel):
    query: str
    response: str
    model_id: str