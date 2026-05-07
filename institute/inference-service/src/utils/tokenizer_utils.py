from transformers import PreTrainedTokenizer

from schemas.inference import ConversationDTO

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
        ).strip()

    @classmethod
    def build_chat_prompt_to_tokens_list(
            cls,
            prompt: str,
            tokenizer: PreTrainedTokenizer,
            conversation_history: list[ConversationDTO],
            system_prompt: str,
    ) -> list:
        messages = [{"role": "system", "content": system_prompt}]

        for msg in conversation_history:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": prompt})

        token_ids = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
        )

        return token_ids