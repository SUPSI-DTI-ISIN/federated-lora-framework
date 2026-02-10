import torch

from typing import Optional
from peft import PeftModel, get_peft_model
from transformers import AutoTokenizer, AutoModelForCausalLM, PreTrainedTokenizer

from federated_learning_common.config import settings


class ModelService:
    @staticmethod
    def load_model(model_path: str, device_map: str, access_token: Optional[str] = None) -> PeftModel:
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map=device_map,
            dtype=torch.float16,
            #token=access_token
            local_files_only=True,
        )
        """
        for name, param in model.named_parameters():
            if any(k in name.lower() for k in ("layernorm", "layer_norm", "ln_", "bias")) or param.ndim == 0:
                param.data = param.data.to(torch.float32)
            else:
                param.data = param.data.to(torch.float16)

            param.requires_grad = False

        model.gradient_checkpointing_enable()
        model.enable_input_require_grads()

        class CastOutputToFloat(nn.Sequential):
            def forward(self, x): return super().forward(x).to(torch.float32)

        model.lm_head = CastOutputToFloat(model.lm_head)
        """
        model = get_peft_model(model, settings.lora_config)

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