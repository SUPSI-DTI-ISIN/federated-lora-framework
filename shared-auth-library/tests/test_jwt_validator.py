import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from shared_auth_library.jwt_validator import JWTValidator
from shared_auth_library.entities import User


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_validator(**kwargs):
    defaults = dict(keycloak_url="http://keycloak.test", realm="TestRealm")
    defaults.update(kwargs)
    with patch("shared_auth_library.jwt_validator.PyJWKClient"):
        return JWTValidator(**defaults)


def _credentials(token="valid.token.here"):
    creds = MagicMock(spec=HTTPAuthorizationCredentials)
    creds.credentials = token
    return creds


def _jwt_payload(**kwargs):
    defaults = {
        "sub": "user-123",
        "preferred_username": "jdoe",
        "given_name": "John",
        "family_name": "Doe",
        "email": "john@example.com",
    }
    defaults.update(kwargs)
    return defaults


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

class TestJWTValidatorInit:
    def test_builds_jwks_uri_from_keycloak_url_and_realm(self):
        validator = _make_validator(keycloak_url="http://kc.local", realm="MyRealm")
        assert validator._JWTValidator__jwks_uri == (
            "http://kc.local/realms/MyRealm/protocol/openid-connect/certs"
        )

    def test_issuer_uses_keycloak_url_when_no_global_hostname(self):
        validator = _make_validator(keycloak_url="http://kc.local", realm="MyRealm")
        assert validator._JWTValidator__issuer == "http://kc.local/realms/MyRealm"

    def test_issuer_uses_global_hostname_when_provided(self):
        validator = _make_validator(
            keycloak_url="http://kc.local",
            realm="MyRealm",
            keycloak_global_hostname_url="http://global.kc.example.com",
        )
        assert validator._JWTValidator__issuer == "http://global.kc.example.com/realms/MyRealm"

    def test_default_algorithms_is_rs256(self):
        validator = _make_validator()
        assert validator._JWTValidator__algorithms == ["RS256"]

    def test_custom_algorithms(self):
        validator = _make_validator(algorithms=["RS256", "HS256"])
        assert validator._JWTValidator__algorithms == ["RS256", "HS256"]

    def test_client_id_defaults_to_none(self):
        validator = _make_validator()
        assert validator._JWTValidator__client_id is None

    def test_client_id_can_be_set(self):
        validator = _make_validator(client_id="my-client")
        assert validator._JWTValidator__client_id == "my-client"

    def test_jwks_client_is_created(self):
        with patch("shared_auth_library.jwt_validator.PyJWKClient") as mock_jwks:
            JWTValidator(keycloak_url="http://kc.local", realm="MyRealm")
        mock_jwks.assert_called_once_with(
            "http://kc.local/realms/MyRealm/protocol/openid-connect/certs"
        )


# ---------------------------------------------------------------------------
# __verify_token — success path
# ---------------------------------------------------------------------------

class TestVerifyTokenSuccess:
    def test_returns_payload_on_valid_token(self):
        validator = _make_validator()
        payload = _jwt_payload()

        mock_signing_key = MagicMock()
        validator._JWTValidator__jwks_client.get_signing_key_from_jwt.return_value = mock_signing_key

        with patch("shared_auth_library.jwt_validator.jwt.decode", return_value=payload):
            result = validator._JWTValidator__verify_token("valid.token")

        assert result == payload

    def test_calls_jwt_decode_with_correct_params(self):
        validator = _make_validator(keycloak_url="http://kc.local", realm="Realm")
        mock_signing_key = MagicMock()
        mock_signing_key.key = "the-key"
        validator._JWTValidator__jwks_client.get_signing_key_from_jwt.return_value = mock_signing_key

        with patch("shared_auth_library.jwt_validator.jwt.decode", return_value=_jwt_payload()) as mock_decode:
            validator._JWTValidator__verify_token("my.token")

        mock_decode.assert_called_once()
        call_kwargs = mock_decode.call_args
        assert call_kwargs[0][0] == "my.token"
        assert call_kwargs[0][1] == "the-key"
        assert call_kwargs[1]["algorithms"] == ["RS256"]
        assert call_kwargs[1]["issuer"] == "http://kc.local/realms/Realm"

    def test_audience_is_none_when_no_client_id(self):
        validator = _make_validator()
        mock_signing_key = MagicMock()
        validator._JWTValidator__jwks_client.get_signing_key_from_jwt.return_value = mock_signing_key

        with patch("shared_auth_library.jwt_validator.jwt.decode", return_value=_jwt_payload()) as mock_decode:
            validator._JWTValidator__verify_token("token")

        assert mock_decode.call_args[1]["audience"] is None

    def test_audience_is_client_id_when_set(self):
        validator = _make_validator(client_id="my-app")
        mock_signing_key = MagicMock()
        validator._JWTValidator__jwks_client.get_signing_key_from_jwt.return_value = mock_signing_key

        with patch("shared_auth_library.jwt_validator.jwt.decode", return_value=_jwt_payload()) as mock_decode:
            validator._JWTValidator__verify_token("token")

        assert mock_decode.call_args[1]["audience"] == "my-app"

    def test_verify_aud_false_when_no_client_id(self):
        validator = _make_validator()
        mock_signing_key = MagicMock()
        validator._JWTValidator__jwks_client.get_signing_key_from_jwt.return_value = mock_signing_key

        with patch("shared_auth_library.jwt_validator.jwt.decode", return_value=_jwt_payload()) as mock_decode:
            validator._JWTValidator__verify_token("token")

        options = mock_decode.call_args[1]["options"]
        assert options["verify_aud"] is False

    def test_verify_aud_true_when_client_id_set(self):
        validator = _make_validator(client_id="my-app")
        mock_signing_key = MagicMock()
        validator._JWTValidator__jwks_client.get_signing_key_from_jwt.return_value = mock_signing_key

        with patch("shared_auth_library.jwt_validator.jwt.decode", return_value=_jwt_payload()) as mock_decode:
            validator._JWTValidator__verify_token("token")

        options = mock_decode.call_args[1]["options"]
        assert options["verify_aud"] is True


# ---------------------------------------------------------------------------
# __verify_token — error paths
# ---------------------------------------------------------------------------

class TestVerifyTokenErrors:
    def _validator_with_mock_jwks(self):
        validator = _make_validator()
        mock_signing_key = MagicMock()
        validator._JWTValidator__jwks_client.get_signing_key_from_jwt.return_value = mock_signing_key
        return validator

    def test_raises_401_on_expired_signature(self):
        from jwt.exceptions import ExpiredSignatureError
        validator = self._validator_with_mock_jwks()

        with patch("shared_auth_library.jwt_validator.jwt.decode", side_effect=ExpiredSignatureError()):
            with pytest.raises(HTTPException) as exc_info:
                validator._JWTValidator__verify_token("expired.token")

        assert exc_info.value.status_code == 401
        assert "expired" in exc_info.value.detail.lower()

    def test_raises_401_on_invalid_audience(self):
        from jwt.exceptions import InvalidAudienceError
        validator = self._validator_with_mock_jwks()

        with patch("shared_auth_library.jwt_validator.jwt.decode", side_effect=InvalidAudienceError()):
            with pytest.raises(HTTPException) as exc_info:
                validator._JWTValidator__verify_token("token")

        assert exc_info.value.status_code == 401
        assert "audience" in exc_info.value.detail.lower()

    def test_raises_401_on_invalid_issuer(self):
        from jwt.exceptions import InvalidIssuerError
        validator = self._validator_with_mock_jwks()

        with patch("shared_auth_library.jwt_validator.jwt.decode", side_effect=InvalidIssuerError()):
            with pytest.raises(HTTPException) as exc_info:
                validator._JWTValidator__verify_token("token")

        assert exc_info.value.status_code == 401
        assert "issuer" in exc_info.value.detail.lower()

    def test_raises_401_on_generic_invalid_token(self):
        from jwt.exceptions import InvalidTokenError
        validator = self._validator_with_mock_jwks()

        with patch("shared_auth_library.jwt_validator.jwt.decode",
                   side_effect=InvalidTokenError("bad signature")):
            with pytest.raises(HTTPException) as exc_info:
                validator._JWTValidator__verify_token("token")

        assert exc_info.value.status_code == 401
        assert "Invalid token" in exc_info.value.detail

    def test_raises_500_on_unexpected_exception(self):
        validator = self._validator_with_mock_jwks()

        with patch("shared_auth_library.jwt_validator.jwt.decode",
                   side_effect=RuntimeError("unexpected")):
            with pytest.raises(HTTPException) as exc_info:
                validator._JWTValidator__verify_token("token")

        assert exc_info.value.status_code == 500
        assert "Token validation error" in exc_info.value.detail

    def test_expired_token_has_www_authenticate_header(self):
        from jwt.exceptions import ExpiredSignatureError
        validator = self._validator_with_mock_jwks()

        with patch("shared_auth_library.jwt_validator.jwt.decode", side_effect=ExpiredSignatureError()):
            with pytest.raises(HTTPException) as exc_info:
                validator._JWTValidator__verify_token("token")

        assert exc_info.value.headers.get("WWW-Authenticate") == "Bearer"

    def test_invalid_token_has_www_authenticate_header(self):
        from jwt.exceptions import InvalidTokenError
        validator = self._validator_with_mock_jwks()

        with patch("shared_auth_library.jwt_validator.jwt.decode",
                   side_effect=InvalidTokenError("bad")):
            with pytest.raises(HTTPException) as exc_info:
                validator._JWTValidator__verify_token("token")

        assert exc_info.value.headers.get("WWW-Authenticate") == "Bearer"

    def test_raises_401_when_jwks_client_fails(self):
        validator = _make_validator()
        validator._JWTValidator__jwks_client.get_signing_key_from_jwt.side_effect = RuntimeError("JWKS fetch failed")

        with pytest.raises(HTTPException) as exc_info:
            validator._JWTValidator__verify_token("token")

        assert exc_info.value.status_code == 500


# ---------------------------------------------------------------------------
# get_current_user_required
# ---------------------------------------------------------------------------

class TestGetCurrentUserRequired:
    async def test_returns_user_on_valid_credentials(self):
        validator = _make_validator()
        payload = _jwt_payload()

        with patch.object(validator, "_JWTValidator__verify_token", return_value=payload):
            user = await validator.get_current_user_required(credentials=_credentials())

        assert isinstance(user, User)
        assert user.id == "user-123"
        assert user.username == "jdoe"

    async def test_raises_401_when_credentials_are_none(self):
        validator = _make_validator()

        with pytest.raises(HTTPException) as exc_info:
            await validator.get_current_user_required(credentials=None)

        assert exc_info.value.status_code == 401
        assert "Authentication required" in exc_info.value.detail

    async def test_raises_401_when_credentials_are_falsy(self):
        validator = _make_validator()

        with pytest.raises(HTTPException) as exc_info:
            await validator.get_current_user_required(credentials=False)

        assert exc_info.value.status_code == 401

    async def test_missing_credentials_has_www_authenticate_header(self):
        validator = _make_validator()

        with pytest.raises(HTTPException) as exc_info:
            await validator.get_current_user_required(credentials=None)

        assert exc_info.value.headers.get("WWW-Authenticate") == "Bearer"

    async def test_propagates_http_exception_from_verify_token(self):
        validator = _make_validator()

        with patch.object(validator, "_JWTValidator__verify_token",
                          side_effect=HTTPException(status_code=401, detail="Token has expired")):
            with pytest.raises(HTTPException) as exc_info:
                await validator.get_current_user_required(credentials=_credentials())

        assert exc_info.value.status_code == 401
        assert "expired" in exc_info.value.detail

    async def test_passes_token_from_credentials_to_verify(self):
        validator = _make_validator()
        payload = _jwt_payload()

        with patch.object(validator, "_JWTValidator__verify_token", return_value=payload) as mock_verify:
            await validator.get_current_user_required(credentials=_credentials("my.special.token"))

        mock_verify.assert_called_once_with("my.special.token")

    async def test_maps_payload_to_user_correctly(self):
        validator = _make_validator()
        payload = _jwt_payload(
            sub="u-xyz",
            preferred_username="alice",
            given_name="Alice",
            family_name="Smith",
            email="alice@example.com",
        )

        with patch.object(validator, "_JWTValidator__verify_token", return_value=payload):
            user = await validator.get_current_user_required(credentials=_credentials())

        assert user.id == "u-xyz"
        assert user.username == "alice"
        assert user.first_name == "Alice"
        assert user.last_name == "Smith"
        assert user.email == "alice@example.com"


# ---------------------------------------------------------------------------
# get_current_user_optional
# ---------------------------------------------------------------------------

class TestGetCurrentUserOptional:
    async def test_returns_user_on_valid_credentials(self):
        validator = _make_validator()
        payload = _jwt_payload()

        with patch.object(validator, "_JWTValidator__verify_token", return_value=payload):
            user = await validator.get_current_user_optional(credentials=_credentials())

        assert isinstance(user, User)
        assert user.id == "user-123"

    async def test_returns_none_when_credentials_are_none(self):
        validator = _make_validator()

        result = await validator.get_current_user_optional(credentials=None)

        assert result is None

    async def test_returns_none_when_credentials_are_falsy(self):
        validator = _make_validator()

        result = await validator.get_current_user_optional(credentials=False)

        assert result is None

    async def test_returns_none_on_http_exception(self):
        validator = _make_validator()

        with patch.object(validator, "_JWTValidator__verify_token",
                          side_effect=HTTPException(status_code=401, detail="expired")):
            result = await validator.get_current_user_optional(credentials=_credentials())

        assert result is None

    async def test_returns_none_on_expired_token(self):
        validator = _make_validator()
        mock_signing_key = MagicMock()
        validator._JWTValidator__jwks_client.get_signing_key_from_jwt.return_value = mock_signing_key

        from jwt.exceptions import ExpiredSignatureError
        with patch("shared_auth_library.jwt_validator.jwt.decode",
                   side_effect=ExpiredSignatureError()):
            result = await validator.get_current_user_optional(credentials=_credentials())

        assert result is None

    async def test_passes_token_from_credentials_to_verify(self):
        validator = _make_validator()
        payload = _jwt_payload()

        with patch.object(validator, "_JWTValidator__verify_token", return_value=payload) as mock_verify:
            await validator.get_current_user_optional(credentials=_credentials("opt.token"))

        mock_verify.assert_called_once_with("opt.token")

    async def test_maps_payload_to_user_correctly(self):
        validator = _make_validator()
        payload = _jwt_payload(sub="u-opt", preferred_username="bob")

        with patch.object(validator, "_JWTValidator__verify_token", return_value=payload):
            user = await validator.get_current_user_optional(credentials=_credentials())

        assert user.id == "u-opt"
        assert user.username == "bob"
