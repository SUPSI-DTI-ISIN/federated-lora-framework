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


_torch_cuda_mod = _make_module("torch.cuda")
_torch_cuda_mod.is_available = MagicMock(return_value=False)
_torch_cuda_mod.empty_cache = MagicMock()
_torch_cuda_mod.synchronize = MagicMock()
_torch_cuda_mod.is_bf16_supported = MagicMock(return_value=False)

torch_mod = _make_module("torch")
torch_mod.cuda = _torch_cuda_mod
torch_mod.bfloat16 = "bfloat16"
torch_mod.float16 = "float16"
torch_mod.no_grad = MagicMock(return_value=MagicMock(__enter__=MagicMock(return_value=None), __exit__=MagicMock(return_value=False)))
torch_mod.tensor = MagicMock(return_value=MagicMock())
torch_mod.ones_like = MagicMock(return_value=MagicMock())

class _FakeAutoModel:
    @classmethod
    def from_pretrained(cls, *a, **kw):
        m = MagicMock()
        m.config = MagicMock()
        m.cpu = MagicMock()
        m.device = "cpu"
        m.eval = MagicMock()
        return m

class _FakeAutoTokenizer:
    @classmethod
    def from_pretrained(cls, *a, **kw):
        t = MagicMock()
        t.eos_token_id = 2
        t.pad_token_id = 0
        return t

class _FakeBnBConfig:
    def __init__(self, **kwargs):
        pass

_make_module(
    "transformers",
    AutoModelForCausalLM=_FakeAutoModel,
    AutoTokenizer=_FakeAutoTokenizer,
    BitsAndBytesConfig=_FakeBnBConfig,
    PreTrainedModel=object,
    PreTrainedTokenizer=object,
)

class _FakeTaskType:
    CAUSAL_LM = "CAUSAL_LM"

class _FakePeftModel:
    def save_pretrained(self, path): pass
    def cpu(self): pass

def _fake_get_peft_model(model, config):
    return _FakePeftModel()

_make_module(
    "peft",
    TaskType=_FakeTaskType,
    PeftModel=_FakePeftModel,
    get_peft_model=_fake_get_peft_model,
)
_make_module("peft.tuners")
_make_module("peft.tuners.lora")

_make_module("bitsandbytes")

def _fake_remove_hook(module, recurse=False): pass
def _fake_dispatch_model(model, device_map): return model
def _fake_infer_auto_device_map(model, **kw): return {}
def _fake_get_balanced_memory(model, **kw): return {}

_make_module("accelerate")
_make_module("accelerate.hooks", remove_hook_from_module=_fake_remove_hook)
_make_module(
    "accelerate.utils",
    get_balanced_memory=_fake_get_balanced_memory,
)
import accelerate as _accel_mod
_accel_mod.dispatch_model = _fake_dispatch_model
_accel_mod.infer_auto_device_map = _fake_infer_auto_device_map

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

_redis_asyncio_mod = _make_module("redis.asyncio")
_redis_asyncio_mod.Redis = MagicMock
_redis_asyncio_mod.from_url = MagicMock(return_value=MagicMock())

_redis_mod = _make_module("redis")
_redis_mod.asyncio = _redis_asyncio_mod
_redis_mod.Redis = MagicMock
_redis_mod.from_url = MagicMock(return_value=MagicMock())

class _FakeJWTValidator:
    def __init__(self, **kwargs): pass
    async def get_current_user_required(self): return MagicMock()

class _FakeUser:
    pass

_make_module("shared_auth_library")
_make_module("shared_auth_library.jwt_validator", JWTValidator=_FakeJWTValidator)
_make_module("shared_auth_library.entities", User=_FakeUser)

os.environ.setdefault("REDIS_URL", "redis://localhost:6379")
os.environ.setdefault("INSTITUTE_NAME", "TestInstitute")
os.environ.setdefault("KEYCLOAK_URL", "http://keycloak.test")
os.environ.setdefault("KEYCLOAK_GLOBAL_HOSTNAME_URL", "")
os.environ.setdefault("MODEL_SERVICE_URL", "http://localhost:8090")
os.environ.setdefault("FRONTEND_URL", "http://localhost:3000")
os.environ.setdefault("DEVICE_MAP", "cpu")
