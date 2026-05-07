from pydantic import BaseModel


class UpdateSectionRequestDTO(BaseModel):
    updated_content: str