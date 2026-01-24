from typing import List

from pydantic import BaseModel


class NewAdapterPath(BaseModel):
    new_adapter_path: str