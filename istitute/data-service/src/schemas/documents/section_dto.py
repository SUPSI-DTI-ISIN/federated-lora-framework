from pydantic import BaseModel, ConfigDict


class SectionDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    content: str