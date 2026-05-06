from typing import List

from pydantic import BaseModel, ConfigDict

from .section_dto import SectionDTO


class UpdateDocumentExternallyApprovedRequestDTO(BaseModel):
    is_externally_approved: bool