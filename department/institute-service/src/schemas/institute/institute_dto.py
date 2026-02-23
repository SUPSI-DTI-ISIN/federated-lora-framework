from pydantic import BaseModel, ConfigDict

class InstituteDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    url: str
    deletable: bool