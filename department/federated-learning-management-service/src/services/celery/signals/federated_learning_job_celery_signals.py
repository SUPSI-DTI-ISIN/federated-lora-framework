from celery.signals import task_success, task_failure
from celery.utils.log import get_task_logger
from clients.redis.client import redis_client_sync
from commons import RedisChannel
from schemas.celery import CeleryJobDTO, CeleryJobResultType

logger = get_task_logger(__name__)

@task_success.connect
def federated_learning_celery_job_success_signal(sender, result, **kwargs):
    task_id = sender.request.id
    payload = CeleryJobDTO(job_id=task_id, result_type=CeleryJobResultType.SUCCESS, result=result)
    redis_client_sync.publish(RedisChannel.JOB_UPDATES.value, payload.model_dump_json())

@task_failure.connect
def federated_learning_celery_job_failure_signal(sender, task_id, exception, args, kwargs, traceback, einfo, **kw):
    payload = CeleryJobDTO(job_id=task_id, result_type=CeleryJobResultType.FAILURE, error=str(exception))
    redis_client_sync.publish(RedisChannel.JOB_UPDATES.value, payload.model_dump_json())