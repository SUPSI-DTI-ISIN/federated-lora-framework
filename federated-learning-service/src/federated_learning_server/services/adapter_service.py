import os
import shutil

from safetensors.torch import load_file, save_file
from torch import Tensor


class AdapterService:
    @classmethod
    def load_adapter_state_dict(cls, adapter_path: str) -> dict[str, Tensor]:
        safetensors_path = os.path.join(adapter_path, "adapter_model.safetensors")

        if os.path.exists(safetensors_path):
            return load_file(safetensors_path, device="cpu")

        raise FileNotFoundError(
            f"No adapter weights found at '{adapter_path}'."
        )

    @classmethod
    def save_adapter(cls, state_dict: dict[str, Tensor], new_adapter_path: str, source_adapter_path: str) -> None:
        os.makedirs(new_adapter_path, exist_ok=True)

        shutil.copy(
            os.path.join(source_adapter_path, "adapter_config.json"),
            os.path.join(new_adapter_path, "adapter_config.json")
        )

        save_file(state_dict, os.path.join(new_adapter_path, "adapter_model.safetensors"))