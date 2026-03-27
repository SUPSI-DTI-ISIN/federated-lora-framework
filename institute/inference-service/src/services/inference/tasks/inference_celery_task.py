from celery.utils.log import get_task_logger

from clients.celery import celery
from clients.model_service import ModelServiceClientInterface, ModelServiceClient
from config import settings
from schemas.inference import QueryRequestDTO, QueryResponseDTO
from services.model import ModelServiceInterface, ModelService
from utils import TokenizerUtils, ModelResponseUtils

logger = get_task_logger(__name__)

@celery.task(bind=True)
def inference_celery_task(self, query_request_dto):
    task_id = self.request.id
    logger.info("Starting Inference task %s", task_id)

    query_request_dto = QueryRequestDTO.model_validate_json(query_request_dto)

    model_service_client: ModelServiceClientInterface = ModelServiceClient.get_instance(model_service_url=settings.model_service_url)
    model_service: ModelServiceInterface = ModelService.get_instance(model_service_client=model_service_client, max_cached_models=settings.max_cached_models, device_map=settings.device_map)
    loaded_model = model_service.get_or_load_model(model_key=query_request_dto.model_key, adapter_version=query_request_dto.adapter_version)

    print(query_request_dto.conversation_history)

    prompt_ids = TokenizerUtils.prompt_to_tokens_list(prompt=query_request_dto.prompt, tokenizer=loaded_model.tokenizer)

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