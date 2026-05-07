from typing import List, Optional

from pydantic import BaseModel

from .adapter_dto import AdapterDTO


class AvailableAdaptersDTO(BaseModel):
    model_key: str
    adapters: Optional[List[AdapterDTO]] = None