from celery.utils.log import get_task_logger

from clients.celery import get_celery_client_service
from config import settings
from schemas.inference import QueryRequestDTO, QueryResponseDTO
from services.model import ModelServiceInterface, build_model_service
from utils import TokenizerUtils, ModelResponseUtils

logger = get_task_logger(__name__)

celery = get_celery_client_service().get_celery_client()

@celery.task(bind=True)
def inference_celery_task(self, query_request_dto):
    task_id = self.request.id
    logger.info("Starting Inference task %s", task_id)

    query_request_dto = QueryRequestDTO.model_validate_json(query_request_dto)

    model_service: ModelServiceInterface = build_model_service()
    loaded_model = model_service.get_or_load_model(model_key=query_request_dto.model_key, adapter_version=query_request_dto.adapter_version)

    prompt_ids = TokenizerUtils.build_chat_prompt_to_tokens_list(
        prompt=query_request_dto.prompt,
        tokenizer=loaded_model.tokenizer,
        conversation_history=query_request_dto.conversation_history,
        system_prompt=settings.model_system_prompt_with_adapter_active if loaded_model.has_adapter else settings.model_system_prompt_without_adapter,
    )

    response_ids = ModelResponseUtils.generate_model_response(prompt_ids=prompt_ids, model=loaded_model.model, tokenizer=loaded_model.tokenizer)

    output = TokenizerUtils.response_ids_to_str(token_ids=response_ids, tokenizer=loaded_model.tokenizer)

    query_response_dto = QueryResponseDTO(
        user_id=query_request_dto.user_id,
        chat_id=query_request_dto.chat_id,
        prompt=query_request_dto.prompt,
        adapter_version=query_request_dto.adapter_version if loaded_model.has_adapter else None,
        response=output,
        model_key=query_request_dto.model_key
    )

    return query_response_dto.model_dump_json()