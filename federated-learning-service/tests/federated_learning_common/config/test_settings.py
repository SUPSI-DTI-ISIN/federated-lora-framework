class TestCommonSettings:
    def _make(self, **kwargs):
        from src.federated_learning_common.config.settings import Settings
        return Settings(**kwargs)

    def test_defaults(self):
        s = self._make()
        assert s.rank == 8
        assert s.lora_alpha == 16
        assert s.lora_dropout == 0.05

    def test_explicit_values(self):
        s = self._make(rank=16, lora_alpha=32, lora_dropout=0.1)
        assert s.rank == 16
        assert s.lora_alpha == 32
        assert s.lora_dropout == 0.1

    def test_lora_config_property_returns_lora_config(self):
        from peft import LoraConfig
        s = self._make()
        config = s.lora_config
        assert isinstance(config, LoraConfig)

    def test_lora_config_uses_rank(self):
        s = self._make(rank=16)
        config = s.lora_config
        assert config.r == 16

    def test_lora_config_uses_lora_alpha(self):
        s = self._make(lora_alpha=32)
        config = s.lora_config
        assert config.lora_alpha == 32

    def test_lora_config_uses_lora_dropout(self):
        s = self._make(lora_dropout=0.1)
        config = s.lora_config
        assert config.lora_dropout == 0.1

    def test_lora_config_target_modules(self):
        s = self._make()
        config = s.lora_config
        assert "q_proj" in config.target_modules
        assert "k_proj" in config.target_modules
        assert "v_proj" in config.target_modules
        assert "o_proj" in config.target_modules

    def test_lora_config_bias_is_none(self):
        s = self._make()
        config = s.lora_config
        assert config.bias == "none"


class TestCommonConfigInit:
    def test_settings_exported(self):
        from src.federated_learning_common.config import settings
        assert settings is not None
        assert hasattr(settings, "rank")

    def test_version(self):
        from src.federated_learning_common.config import __version__
        assert __version__ == "1.0.0"
