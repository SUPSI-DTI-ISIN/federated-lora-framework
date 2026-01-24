from pydantic import BaseModel


class AdapterDTO(BaseModel):
    version: int
    available_local: bool