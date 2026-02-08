from typing import Any

from shared_auth_library.entities import User


class JWTToUserMapperUtils:
    @classmethod
    def jwt_to_user(cls, payload: dict[str, Any]) -> User:
        return User(
            id=payload.get("sub", ""),
            username=payload.get("preferred_username", ""),
            first_name=payload.get("given_name", ""),
            last_name=payload.get("family_name", ""),
            email=payload.get("email", ""),
            ray_payload=payload
        )