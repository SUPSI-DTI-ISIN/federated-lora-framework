from typing import Optional, Dict, Any, Annotated
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWKClient
from jwt.exceptions import (
    InvalidTokenError,
    ExpiredSignatureError,
    InvalidAudienceError,
    InvalidIssuerError
)

from shared_auth_library.entities import User
from shared_auth_library.utils import JWTToUserMapperUtils

security = HTTPBearer(auto_error=False)

class JWTValidator:
    def __init__(
            self,
            keycloak_url: str,
            realm: str,
            client_id: Optional[str] = None,
            algorithms: list[str] = None
    ):
        self.__keycloak_url = keycloak_url
        self.__realm = realm
        self.__client_id = client_id
        self.__algorithms = algorithms or ["RS256"]
        self.__jwks_uri = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/certs"
        self.__issuer = f"{keycloak_url}/realms/{realm}"

        self.__jwks_client = PyJWKClient(self.__jwks_uri)

    def __verify_token(self, token: str) -> Dict[str, Any]:
        try:
            signing_key = self.__jwks_client.get_signing_key_from_jwt(token)

            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=self.__algorithms,
                issuer=self.__issuer,
                audience=self.__client_id if self.__client_id else None,
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_nbf": True,
                    "verify_iat": True,
                    "verify_aud": bool(self.__client_id),
                    "require_exp": True,
                    "require_iat": True,
                }
            )
            return payload

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except InvalidAudienceError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token audience"
            )
        except InvalidIssuerError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token issuer"
            )
        except InvalidTokenError as e:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid token: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Token validation error: {str(e)}"
            )

    async def get_current_user_optional(
            self,
            credentials: Annotated[Optional[HTTPAuthorizationCredentials], Security(security)]
    ) -> Optional[User]:
        if not credentials:
            return None

        try:
            token = credentials.credentials
            jwt_payload = self.__verify_token(token)
            return JWTToUserMapperUtils.jwt_to_user(payload=jwt_payload)
        except HTTPException:
            return None

    async def get_current_user_required(
            self,
            credentials: Annotated[HTTPAuthorizationCredentials, Security(security)]
    ) -> User:
        if not credentials:
            raise HTTPException(
                status_code=401,
                detail="Authentication required",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = credentials.credentials
        jwt_payload = self.__verify_token(token)
        return JWTToUserMapperUtils.jwt_to_user(payload=jwt_payload)