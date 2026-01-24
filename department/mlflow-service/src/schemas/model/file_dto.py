from pydantic import BaseModel


class FileDTO(BaseModel):
    size: int
    rel_path: str
    hash: str