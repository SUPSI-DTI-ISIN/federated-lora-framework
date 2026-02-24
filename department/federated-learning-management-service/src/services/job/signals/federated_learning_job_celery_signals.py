from celery.signals import task_success, task_failure
from celery.utils.log import get_task_logger
from clients.redis import redis_client_sync
from commons import RedisChannel
from schemas.job import FederatedLearningJobDTO, FederatedLearningJobResultType

logger = get_task_logger(__name__)

@task_success.connect
def federated_learning_celery_job_success_signal(sender, result, **kwargs):
    task_id = sender.request.id
    payload = FederatedLearningJobDTO(job_id=task_id, result_type=FederatedLearningJobResultType.SUCCESS, result=result)
    redis_client_sync.publish(RedisChannel.JOB_UPDATES.value, payload.model_dump_json())

@task_failure.connect
def federated_learning_celery_job_failure_signal(sender, task_id, exception, args, kwargs, traceback, einfo, **kw):
    payload = FederatedLearningJobDTO(job_id=task_id, result_type=FederatedLearningJobResultType.FAILURE, error=str(exception))
    redis_client_sync.publish(RedisChannel.JOB_UPDATES.value, payload.model_dump_json())