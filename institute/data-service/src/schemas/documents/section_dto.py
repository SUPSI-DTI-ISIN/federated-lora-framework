from pydantic import BaseModel, ConfigDict


class SectionDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str