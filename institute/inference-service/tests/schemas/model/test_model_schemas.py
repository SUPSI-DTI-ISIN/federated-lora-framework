from datetime import datetime, timezone
from unittest.mock import MagicMock
from schemas.model import LoadedModel, ModelCacheKey


class TestModelCacheKey:
    def test_equality(self):
        k1 = ModelCacheKey(model_key="llama", adapter_version="v1")
        k2 = ModelCacheKey(model_key="llama", adapter_version="v1")
        assert k1 == k2

    def test_inequality_different_key(self):
        k1 = ModelCacheKey(model_key="llama", adapter_version="v1")
        k2 = ModelCacheKey(model_key="mistral", adapter_version="v1")
        assert k1 != k2

    def test_inequality_different_adapter(self):
        k1 = ModelCacheKey(model_key="llama", adapter_version="v1")
        k2 = ModelCacheKey(model_key="llama", adapter_version="v2")
        assert k1 != k2

    def test_hashable(self):
        k = ModelCacheKey(model_key="llama", adapter_version="v1")
        assert hash(k) == hash(("llama", "v1"))

    def test_usable_as_dict_key(self):
        k = ModelCacheKey(model_key="llama", adapter_version="v1")
        d = {k: "value"}
        assert d[k] == "value"

    def test_none_adapter_version(self):
        k = ModelCacheKey(model_key="llama", adapter_version=None)
        assert k.adapter_version is None


class TestLoadedModel:
    def test_can_be_created(self):
        model = MagicMock()
        tokenizer = MagicMock()
        now = datetime.now(timezone.utc)
        lm = LoadedModel(model=model, tokenizer=tokenizer, has_adapter=True, loaded_at=now)
        assert lm.model is model
        assert lm.tokenizer is tokenizer
        assert lm.has_adapter is True
        assert lm.loaded_at is now

    def test_has_adapter_false(self):
        lm = LoadedModel(
            model=MagicMock(), tokenizer=MagicMock(),
            has_adapter=False, loaded_at=datetime.now(timezone.utc)
        )
        assert lm.has_adapter is False

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(LoadedModel)


class TestSchemaModelInit:
    def test_exports(self):
        import schemas.model as sm
        assert "LoadedModel" in sm.__all__
        assert "ModelCacheKey" in sm.__all__

    def test_version(self):
        import schemas.model as sm
        assert sm.__version__ == "1.0.0"
