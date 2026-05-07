from fastapi import UploadFile, File, Form
from pydantic import BaseModel, ConfigDict


class UploadDocumentRequestDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    is_externally_approved: bool
    file: UploadFile

    @classmethod
    def as_form(
            cls,
            is_externally_approved: bool = Form(..., description="Whether the document has been approved by an external entity"),
            file: UploadFile = File(..., description="PDF file to upload")
    ) -> "UploadDocumentRequestDTO":
        instance = cls(is_externally_approved=is_externally_approved, file=file)
        return instance