from dataclasses import dataclass
from typing import Any


@dataclass
class User:
    id: str
    username: str
    first_name: str
    last_name: str
    email: str
    ray_payload: dict[str, Any]