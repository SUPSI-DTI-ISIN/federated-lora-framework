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


# --- redis stubs ---
_redis_asyncio_mod = _make_module("redis.asyncio")
_redis_asyncio_mod.Redis = MagicMock
_redis_asyncio_mod.from_url = MagicMock(return_value=MagicMock())

_redis_mod = _make_module("redis")
_redis_mod.asyncio = _redis_asyncio_mod
_redis_mod.Redis = MagicMock
_redis_mod.from_url = MagicMock(return_value=MagicMock())

# --- sse_starlette stubs ---
_sse_mod = _make_module("sse_starlette")
_sse_mod.EventSourceResponse = MagicMock
_sse_mod.ServerSentEvent = MagicMock

# --- shared_auth_library stubs ---
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
os.environ.setdefault("REALM_NAME", "TestRealm")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379")
os.environ.setdefault("INSTITUTE_NAME", "TestInstitute")
os.environ.setdefault("FRONTEND_URL", "http://localhost:3000")
os.environ.setdefault("INFERENCE_SERVICE_URL", "http://localhost:8095")
os.environ.setdefault("KEYCLOAK_GLOBAL_HOSTNAME_URL", "")


@pytest.fixture()
def mock_chat_service():
    return MagicMock()


@pytest.fixture()
def mock_message_service():
    return MagicMock()


@pytest.fixture()
def mock_inference_service():
    return MagicMock()


@pytest.fixture()
def mock_sse_service():
    return MagicMock()
