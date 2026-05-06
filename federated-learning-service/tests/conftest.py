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


_torch_cuda = _make_module("torch.cuda")
_torch_cuda.is_available = MagicMock(return_value=False)
_torch_cuda.is_bf16_supported = MagicMock(return_value=False)
_torch_cuda.empty_cache = MagicMock()

torch_mod = _make_module("torch")
torch_mod.cuda = _torch_cuda
torch_mod.bfloat16 = "bfloat16"
torch_mod.float16 = "float16"
torch_mod.Tensor = MagicMock


class _FakeAutoModel:
    @classmethod
    def from_pretrained(cls, *a, **kw):
        m = MagicMock()
        m.config = MagicMock()
        m.named_parameters = MagicMock(return_value=[])
        return m

class _FakeAutoTokenizer:
    @classmethod
    def from_pretrained(cls, *a, **kw):
        t = MagicMock()
        t.pad_token = None
        t.eos_token = "<eos>"
        return t

class _FakeBnBConfig:
    def __init__(self, **kwargs): pass

class _FakeTrainingArguments:
    def __init__(self, *a, **kw): pass

class _FakeTrainer:
    def __init__(self, *a, **kw): pass
    def train(self):
        r = MagicMock()
        r.metrics = {"train_loss": 0.5}
        return r
    def evaluate(self):
        return {"eval_loss": 1.0}

class _FakeDataCollator:
    def __init__(self, *a, **kw): pass

_make_module(
    "transformers",
    AutoModelForCausalLM=_FakeAutoModel,
    AutoTokenizer=_FakeAutoTokenizer,
    BitsAndBytesConfig=_FakeBnBConfig,
    TrainingArguments=_FakeTrainingArguments,
    Trainer=_FakeTrainer,
    DataCollatorForLanguageModeling=_FakeDataCollator,
    PreTrainedModel=object,
    PreTrainedTokenizer=object,
)


class _FakeTaskType:
    CAUSAL_LM = "CAUSAL_LM"

class _FakeLoraConfig:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class _FakePeftModel:
    def save_pretrained(self, path): pass
    def cpu(self): pass
    @classmethod
    def from_pretrained(cls, model, path, **kw):
        return cls()

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


_make_module("bitsandbytes")


_make_module("accelerate")
_make_module("accelerate.hooks", remove_hook_from_module=MagicMock())
_make_module("accelerate.utils", get_balanced_memory=MagicMock(return_value={}))


class _FakeDataset:
    def __init__(self, data=None):
        self._data = data or {}
        self.column_names = list(self._data.keys()) if self._data else []
    def map(self, fn, **kw): return self
    def train_test_split(self, **kw):
        return {"train": self, "test": self}
    def __len__(self): return 10

_fake_split = MagicMock()
_fake_split.TRAIN = "train"

_datasets_mod = _make_module(
    "datasets",
    load_dataset=MagicMock(return_value=_FakeDataset()),
    Split=_fake_split,
)


_safetensors_torch = _make_module(
    "safetensors.torch",
    load_file=MagicMock(return_value={"weight": MagicMock()}),
    save_file=MagicMock(),
)
_make_module("safetensors", torch=_safetensors_torch)


_make_module("flwr")
_make_module("flwr.app", ArrayRecord=MagicMock(), ConfigRecord=MagicMock(), Context=MagicMock())
_make_module("flwr.serverapp", Grid=MagicMock(), ServerApp=MagicMock())
_make_module("flwr.serverapp.strategy", FedAvg=MagicMock())


_make_module("superexec")


os.environ.setdefault("DATA_SERVICE_URL", "http://localhost:8080")
os.environ.setdefault("MODEL_SERVICE_URL", "http://localhost:8090")
os.environ.setdefault("DEVICE_MAP", "cpu")
os.environ.setdefault("MODEL_KEY", "llama-2-7b")
os.environ.setdefault("DATASET_OUTPUT_FOLDER", "/tmp/fl_output")
os.environ.setdefault("MLFLOW_SERVICE_URL", "http://localhost:9010")
