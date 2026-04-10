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
        )

    @classmethod
    def build_chat_prompt_to_tokens_list(
            cls,
            prompt: str,
            tokenizer: PreTrainedTokenizer,
            conversation_history: list[ConversationDTO],
            system_prompt: str,
    ) -> list:
        turns: list[tuple[str, str]] = []
        pending_user: str | None = None

        for msg in conversation_history:
            if msg.role == "user":
                pending_user = msg.content
            elif msg.role == "assistant" and pending_user is not None:
                turns.append((pending_user, msg.content))
                pending_user = None

        parts: list[str] = []

        for i, (user_msg, assistant_msg) in enumerate(turns):
            if i == 0:
                user_block = f"<<SYS>>\n{system_prompt}\n<</SYS>>\n\n{user_msg}"
            else:
                user_block = user_msg

            parts.append(f"<s>[INST] {user_block} [/INST] {assistant_msg} </s>")

        if not turns:
            current_block = f"<<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt}"
        else:
            current_block = prompt

        parts.append(f"<s>[INST] {current_block} [/INST]")

        full_prompt = "".join(parts)

        token_ids = tokenizer(full_prompt, return_tensors="np")["input_ids"]
        return token_ids[0].tolist()