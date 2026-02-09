from typing import Optional

import torch

from peft import PeftModel, get_peft_model
from torch import nn
from transformers import AutoTokenizer, AutoModelForCausalLM, PreTrainedTokenizer

from federated_learning_common.config import settings


class ModelService:
    @staticmethod
    def load_model(model_path: str, device_map: str, access_token: Optional[str] = None) -> PeftModel:
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map=device_map,
            torch_dtype=torch.float16,
            #token=access_token
            local_files_only=True,
        )

        for param in model.parameters():
            param.requires_grad = False
            if param.ndim == 1:
                param.data = param.data.to(torch.float16)

        model.gradient_checkpointing_disable()
        model.enable_input_require_grads()

        class CastOutputToFloat(nn.Sequential):
            def forward(self, x): return super().forward(x).to(torch.float16)

        model.lm_head = CastOutputToFloat(model.lm_head)

        model = get_peft_model(model, settings.lora_config)

        model.eval()

        return model

    @staticmethod
    def load_tokenizer(model_path: str, access_token: Optional[str] = None) -> PreTrainedTokenizer:
        tokenizer = AutoTokenizer.from_pretrained(model_path,
                                                  #token=access_token
                                                  local_files_only=True
                                                  )
        tokenizer.pad_token = tokenizer.eos_token
        return tokenizer

    @staticmethod
    def print_trainable_parameters(model):
        trainable_params = 0
        all_param = 0
        for _, param in model.named_parameters():
            all_param += param.numel()
            if param.requires_grad:
                trainable_params += param.numel()

        print(
            f"Trainable parameters: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param:.2f}%")