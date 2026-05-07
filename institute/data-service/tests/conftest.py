import os
import sys
import types
from unittest.mock import MagicMock

import pytest


def _make_module(name: str, **attrs) -> types.ModuleType:
    mod = types.ModuleType(name)
    for k, v in attrs.items():
        setattr(mod, k, v)
    sys.modules.setdefault(name, mod)
    return mod


class _FakeJWTValidator:
    def __init__(self, **kwargs):
        pass

    async def get_current_user_required(self):
        return MagicMock()


class _FakeUser:
    pass


_make_module("shared_auth_library")
_make_module("shared_auth_library.jwt_validator", JWTValidator=_FakeJWTValidator)
_make_module("shared_auth_library.entities", User=_FakeUser)

os.environ.setdefault("KEYCLOAK_URL", "http://keycloak.test")
os.environ.setdefault("INSTITUTE_NAME", "TestInstitute")
os.environ.setdefault("FRONTEND_URL", "http://localhost:3000")
os.environ.setdefault("KEYCLOAK_GLOBAL_HOSTNAME_URL", "")


@pytest.fixture()
def mock_documents_repository():
    from unittest.mock import AsyncMock
    return AsyncMock()


@pytest.fixture()
def mock_sections_repository():
    from unittest.mock import AsyncMock
    return AsyncMock()
