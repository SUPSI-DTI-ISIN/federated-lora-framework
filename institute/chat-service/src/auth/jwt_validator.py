from shared_auth_library.jwt_validator import JWTValidator

from config import settings

jwt_validator = JWTValidator(
    keycloak_url=settings.keycloak_url,
    realm=settings.institute_name
)