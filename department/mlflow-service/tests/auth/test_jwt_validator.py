import pytest


class TestJwtValidatorModule:
    def test_jwt_validator_is_exported(self):
        from auth import jwt_validator
        assert jwt_validator is not None

    def test_jwt_validator_version(self):
        import auth
        assert auth.__version__ == "1.0.0"

    def test_jwt_validator_is_correct_type(self):
        from auth import jwt_validator
        from shared_auth_library.jwt_validator import JWTValidator
        assert isinstance(jwt_validator, JWTValidator)

    def test_jwt_validator_all_export(self):
        import auth
        assert "jwt_validator" in auth.__all__
