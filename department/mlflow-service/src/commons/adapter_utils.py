from pathlib import Path


class AdapterUtils:
    @classmethod
    def is_valid_adapter(cls, path: Path) -> bool:
        return (
                path.exists()
                and (path / "adapter_config.json").exists()
                and (path / "adapter_model.safetensors").exists()
        )