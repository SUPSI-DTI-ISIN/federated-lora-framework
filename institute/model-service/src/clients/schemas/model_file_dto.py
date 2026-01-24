from pydantic import BaseModel


class ModelFileDTO(BaseModel):
    size: int
    rel_path: str
    hash: str