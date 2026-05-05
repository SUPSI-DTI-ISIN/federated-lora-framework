import os
import sys
import types
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel as _PydanticBase, ConfigDict


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

torch_mod = _make_module("torch")
torch_mod.cuda = _torch_cuda_mod
torch_mod.bfloat16 = "bfloat16"
torch_mod.float16 = "float16"


class _FakeTaskType:
    CAUSAL_LM = "CAUSAL_LM"


class _FakeLoraConfig(_PydanticBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    r: int = 8
    lora_alpha: int = 16
    lora_dropout: float = 0.05
    bias: str = "none"
    task_type: str = "CAUSAL_LM"
    target_modules: list = []


class _FakePeftModel:
    def save_pretrained(self, path):
        pass

    def cpu(self):
        pass


def _fake_get_peft_model(model, config):
    return _FakePeftModel()


_make_module(
    "peft",
    TaskType=_FakeTaskType,
    LoraConfig=_FakeLoraConfig,
    PeftModel=_FakePeftModel,
    get_peft_model=_fake_get_peft_model,
)
_make_module("peft.tuners")
_make_module("peft.tuners.lora")


class _FakeAutoModel:
    @classmethod
    def from_pretrained(cls, *a, **kw):
        m = MagicMock()
        m.config = MagicMock()
        m.cpu = MagicMock()
        return m


class _FakeBnBConfig:
    def __init__(self, **kwargs):
        pass


_make_module(
    "transformers",
    AutoModelForCausalLM=_FakeAutoModel,
    BitsAndBytesConfig=_FakeBnBConfig,
    PreTrainedModel=object,
)

_make_module("bitsandbytes")


def _fake_remove_hook(module, recurse=False):
    pass


_make_module("accelerate")
_make_module("accelerate.hooks", remove_hook_from_module=_fake_remove_hook)


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


os.environ.setdefault("MODEL_KEY", "test-model")
os.environ.setdefault("KEYCLOAK_URL", "http://keycloak.test")
os.environ.setdefault("REALM_NAME", "TestRealm")
os.environ.setdefault("MODEL_BASE_PATH", "/tmp/models")
os.environ.setdefault("DEVICE_MAP", "cpu")
os.environ.setdefault("FRONTEND_URL", "http://localhost:3001")


@pytest.fixture()
def mock_adapter_service():
    svc = MagicMock()
    svc.get_new_adapter_path.return_value = "/tmp/models/test-model/adapters/2"
    svc.get_latest_adapter_path.return_value = "/tmp/models/test-model/adapters/1"
    return svc


@pytest.fixture()
def mock_model_service():
    return MagicMock()
