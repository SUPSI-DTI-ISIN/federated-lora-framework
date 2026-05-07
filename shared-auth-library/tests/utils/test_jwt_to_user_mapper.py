from shared_auth_library.entities import User
from shared_auth_library.utils import JWTToUserMapperUtils


class TestJWTToUserMapperUtils:
    def _payload(self, **kwargs):
        defaults = {
            "sub": "user-abc",
            "preferred_username": "jdoe",
            "given_name": "John",
            "family_name": "Doe",
            "email": "john.doe@example.com",
        }
        defaults.update(kwargs)
        return defaults

    def test_maps_all_fields_correctly(self):
        payload = self._payload()
        user = JWTToUserMapperUtils.jwt_to_user(payload=payload)

        assert isinstance(user, User)
        assert user.id == "user-abc"
        assert user.username == "jdoe"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"

    def test_ray_payload_is_full_jwt_payload(self):
        payload = self._payload(extra_claim="value")
        user = JWTToUserMapperUtils.jwt_to_user(payload=payload)
        assert user.ray_payload is payload

    def test_missing_sub_defaults_to_empty_string(self):
        payload = self._payload()
        del payload["sub"]
        user = JWTToUserMapperUtils.jwt_to_user(payload=payload)
        assert user.id == ""

    def test_missing_preferred_username_defaults_to_empty_string(self):
        payload = self._payload()
        del payload["preferred_username"]
        user = JWTToUserMapperUtils.jwt_to_user(payload=payload)
        assert user.username == ""

    def test_missing_given_name_defaults_to_empty_string(self):
        payload = self._payload()
        del payload["given_name"]
        user = JWTToUserMapperUtils.jwt_to_user(payload=payload)
        assert user.first_name == ""

    def test_missing_family_name_defaults_to_empty_string(self):
        payload = self._payload()
        del payload["family_name"]
        user = JWTToUserMapperUtils.jwt_to_user(payload=payload)
        assert user.last_name == ""

    def test_missing_email_defaults_to_empty_string(self):
        payload = self._payload()
        del payload["email"]
        user = JWTToUserMapperUtils.jwt_to_user(payload=payload)
        assert user.email == ""

    def test_empty_payload_returns_user_with_empty_strings(self):
        user = JWTToUserMapperUtils.jwt_to_user(payload={})
        assert user.id == ""
        assert user.username == ""
        assert user.first_name == ""
        assert user.last_name == ""
        assert user.email == ""

    def test_extra_claims_preserved_in_ray_payload(self):
        payload = self._payload(realm_access={"roles": ["admin"]}, azp="my-client")
        user = JWTToUserMapperUtils.jwt_to_user(payload=payload)
        assert user.ray_payload["realm_access"] == {"roles": ["admin"]}
        assert user.ray_payload["azp"] == "my-client"


class TestUtilsInit:
    def test_exports_jwt_to_user_mapper_utils(self):
        from shared_auth_library.utils import JWTToUserMapperUtils as M
        assert M is JWTToUserMapperUtils

    def test_version(self):
        from shared_auth_library.utils import __version__
        assert __version__ == "1.0.0"

    def test_all_list(self):
        from shared_auth_library import utils
        assert "JWTToUserMapperUtils" in utils.__all__
