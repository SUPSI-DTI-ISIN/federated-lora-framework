from pydantic import BaseModel


class NewAdapterRequestDTO(BaseModel):
    version: int