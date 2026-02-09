from typing import List

from pydantic import BaseModel, ConfigDict

from .section_dto import SectionDTO


class DocumentDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    number: str
    title: str
    sections: List[SectionDTO]