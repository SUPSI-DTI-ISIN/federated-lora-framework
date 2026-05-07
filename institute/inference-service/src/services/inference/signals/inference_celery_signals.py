from celery.signals import task_success, task_failure
from celery.utils.log import get_task_logger
from clients.redis import get_redis_client_sync
from commons import RedisChannel
from schemas.celery import CeleryJobDTO, CeleryJobResultType
from schemas.inference import QueryResponseDTO, QueryRequestDTO

logger = get_task_logger(__name__)

@task_success.connect
def inference_celery_task_success_signal(sender, result, **kwargs):
    task_id = sender.request.id
    query_response_dto = QueryResponseDTO.model_validate_json(result)
    payload = CeleryJobDTO(job_id=task_id, result_type=CeleryJobResultType.SUCCESS, chat_id=query_response_dto.chat_id, result=query_response_dto)

    redis_client_sync = get_redis_client_sync()
    redis_client_sync.publish(f"{RedisChannel.INFERENCE_RESULT.value}:{query_response_dto.user_id}", payload.model_dump_json())

@task_failure.connect
def inference_celery_task_failure_signal(sender, task_id, exception, args, kwargs, traceback, einfo, **kw):
    query_request_dto = QueryRequestDTO.model_validate_json(kwargs.get("query_request_dto"))
    payload = CeleryJobDTO(job_id=task_id, result_type=CeleryJobResultType.FAILURE, chat_id=query_request_dto.chat_id, error=str(exception))

    redis_client_sync = get_redis_client_sync()
    redis_client_sync.publish(f"{RedisChannel.INFERENCE_RESULT.value}:{query_request_dto.user_id}", payload.model_dump_json())