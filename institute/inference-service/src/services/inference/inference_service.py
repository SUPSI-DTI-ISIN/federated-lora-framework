from config import settings
from schemas.inference import QueryResponseDTO, QueryRequestDTO
from schemas.model import LoadedModel
from services.inference.inference_service_interface import InferenceServiceInterface
from utils import ModelResponseUtils, TokenizerUtils

class InferenceService(InferenceServiceInterface):
    __INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE


    async def inference_model(self, query_request_dto: QueryRequestDTO, loaded_model: LoadedModel) -> QueryResponseDTO:
        print(query_request_dto.conversation_history)

        if settings.mock_llm_usage:
            return QueryResponseDTO(
                prompt=query_request_dto.prompt,
                adapter_version=query_request_dto.adapter_version if loaded_model.has_adapter else None,
                response=f"Llm response mocked for prompt",
                model_key=query_request_dto.model_key
            )

        #TODO: Handle conversation history
        prompt_ids = TokenizerUtils.prompt_to_tokens_list(prompt=query_request_dto.prompt, tokenizer=loaded_model.tokenizer)

        response_ids = ModelResponseUtils.generate_model_response(prompt_ids=prompt_ids, model=loaded_model.model)

        output = TokenizerUtils.response_ids_to_str(token_ids=response_ids, tokenizer=loaded_model.tokenizer)

        return QueryResponseDTO(
            prompt=query_request_dto.prompt,
            adapter_version=query_request_dto.adapter_version if loaded_model.has_adapter else None,
            response=output,
            model_key=query_request_dto.model_key
        )