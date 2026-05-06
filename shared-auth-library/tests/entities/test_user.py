import dataclasses
from shared_auth_library.entities import User


class TestUser:
    def _make(self, **kwargs):
        defaults = dict(
            id="user-123",
            username="jdoe",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            ray_payload={"sub": "user-123"},
        )
        defaults.update(kwargs)
        return User(**defaults)

    def test_stores_all_fields(self):
        user = self._make()
        assert user.id == "user-123"
        assert user.username == "jdoe"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.ray_payload == {"sub": "user-123"}

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(User)

    def test_equality(self):
        u1 = self._make()
        u2 = self._make()
        assert u1 == u2

    def test_inequality_different_id(self):
        u1 = self._make(id="a")
        u2 = self._make(id="b")
        assert u1 != u2

    def test_ray_payload_can_be_complex(self):
        payload = {"sub": "u-1", "roles": ["admin", "user"], "nested": {"key": "value"}}
        user = self._make(ray_payload=payload)
        assert user.ray_payload["roles"] == ["admin", "user"]

    def test_empty_strings_are_valid(self):
        user = self._make(id="", username="", first_name="", last_name="", email="")
        assert user.id == ""
        assert user.email == ""


class TestEntitiesInit:
    def test_exports_user(self):
        from shared_auth_library.entities import User as U
        assert U is User

    def test_version(self):
        from shared_auth_library.entities import __version__
        assert __version__ == "1.0.0"

    def test_all_list(self):
        from shared_auth_library import entities
        assert "User" in entities.__all__
