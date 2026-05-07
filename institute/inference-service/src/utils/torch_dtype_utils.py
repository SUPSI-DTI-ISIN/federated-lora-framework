import torch


class TorchDtypeUtils:
    @classmethod
    def get_torch_dtype(cls):
        if torch.cuda.is_available() and getattr(torch.cuda, "is_bf16_supported", lambda: False)():
            return torch.bfloat16
        else:
            return torch.float16