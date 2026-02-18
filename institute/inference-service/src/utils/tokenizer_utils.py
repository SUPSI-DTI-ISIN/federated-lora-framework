from transformers import PreTrainedTokenizer

class TokenizerUtils:
    @classmethod
    def prompt_to_tokens_list(cls, prompt: str, tokenizer: PreTrainedTokenizer) -> list:
        token_ids = tokenizer(prompt, return_tensors="np")["input_ids"]
        return token_ids[0].tolist()

    @classmethod
    def response_ids_to_str(cls, token_ids: list, tokenizer: PreTrainedTokenizer) -> str:
        return tokenizer.decode(
            token_ids,
            skip_special_tokens=True
        )