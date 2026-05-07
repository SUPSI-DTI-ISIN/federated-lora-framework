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


_redis_asyncio_mod = _make_module("redis.asyncio")
_redis_asyncio_mod.Redis = MagicMock
_redis_asyncio_mod.from_url = MagicMock(return_value=MagicMock())

_redis_mod = _make_module("redis")
_redis_mod.asyncio = _redis_asyncio_mod
_redis_mod.Redis = MagicMock
_redis_mod.from_url = MagicMock(return_value=MagicMock())

_fake_celery_app = MagicMock()
_fake_celery_app.task = MagicMock(return_value=lambda f: f)

_celery_mod = _make_module("celery")
_celery_mod.Celery = MagicMock(return_value=_fake_celery_app)

_celery_signals_mod = _make_module("celery.signals")
_celery_signals_mod.task_success = MagicMock()
_celery_signals_mod.task_failure = MagicMock()
_celery_signals_mod.task_success.connect = lambda f: f
_celery_signals_mod.task_failure.connect = lambda f: f

_celery_utils_log_mod = _make_module("celery.utils.log")
_celery_utils_log_mod.get_task_logger = MagicMock(return_value=MagicMock())

_sse_mod = _make_module("sse_starlette")
_sse_mod.EventSourceResponse = MagicMock
_sse_mod.ServerSentEvent = MagicMock

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

_make_module("flwr")

os.environ.setdefault("KEYCLOAK_URL", "http://keycloak.test")
os.environ.setdefault("REALM_NAME", "TestRealm")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379")
os.environ.setdefault("FLWR_APP_BASE_PATH", "/tmp/flwr")
os.environ.setdefault("FEDERATED_LEARNING_DEPLOYMENT_ENVIRONMENT", "local-simulation")
os.environ.setdefault("FRONTEND_URL", "http://localhost:3000")


@pytest.fixture()
def mock_job_service():
    return MagicMock()


@pytest.fixture()
def mock_celery_service():
    return MagicMock()


@pytest.fixture()
def mock_sse_service():
    return MagicMock()
