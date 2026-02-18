import torch

class ModelResponseUtils:
    @classmethod
    def generate_model_response(cls, prompt_ids: list, model) -> list:
        input_ids = torch.tensor( [prompt_ids] , device=model.device)
        attention_mask = torch.ones_like( input_ids )

        with torch.no_grad():
            outputs = model.generate(
                input_ids,
                attention_mask=attention_mask,
                max_new_tokens=256,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
            )

        return outputs[0]