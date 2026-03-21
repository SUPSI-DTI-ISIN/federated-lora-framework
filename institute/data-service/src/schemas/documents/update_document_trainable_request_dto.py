from typing import List

from pydantic import BaseModel, ConfigDict

from .section_dto import SectionDTO


class UpdateDocumentTrainableRequestDTO(BaseModel):
    is_trainable: bool