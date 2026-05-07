import redis.asyncio

from commons import RedisChannel
from entities import FederatedLearningJobStatus
from repositories.federated_learning_job import build_federated_learning_job_repository
from schemas.celery import CeleryJobResultType, CeleryJobDTO
from services.redis import RedisEventConsumerServiceInterface

from database import DatabaseConnector

class FederatedLearningJobRedisEventConsumer(RedisEventConsumerServiceInterface):
    __INSTANCE = None

    def __init__(self, redis_client_async: redis.asyncio.Redis):
        self.__redis_client_async = redis_client_async

    @classmethod
    def get_instance(cls, redis_client_async: redis.asyncio.Redis):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(redis_client_async=redis_client_async)
        return cls.__INSTANCE

    async def start_redis_event_consumer(self):
        pubsub = self.__redis_client_async.pubsub()
        await pubsub.subscribe(RedisChannel.JOB_UPDATES.value)
        try:
            async for message in pubsub.listen():
                if message is None:
                    continue
                if message.get("type") != "message":
                    continue
                try:
                    celery_job_dto = CeleryJobDTO.model_validate_json(message["data"])
                    await self.__update_federated_learning_job(celery_job_dto=celery_job_dto)

                except Exception as e:
                    print(f"Failed to process job update message: {e}")
        finally:
            await pubsub.unsubscribe(RedisChannel.JOB_UPDATES.value)
            await pubsub.close()

    async def __update_federated_learning_job(self, celery_job_dto: CeleryJobDTO) -> None:
        async with DatabaseConnector.get_session_factory()() as session:
            federated_learning_job_repository = build_federated_learning_job_repository(db=session)

            federated_learning_job = await federated_learning_job_repository.get_by_celery_task_id(
                celery_task_id=celery_job_dto.job_id
            )

            if federated_learning_job is None:
                return

            if celery_job_dto.result_type == CeleryJobResultType.SUCCESS:
                federated_learning_job.status = FederatedLearningJobStatus.SUCCESS
            elif celery_job_dto.result_type == CeleryJobResultType.FAILURE:
                federated_learning_job.status = FederatedLearningJobStatus.FAILURE

            await federated_learning_job_repository.save(federated_learning_job_model=federated_learning_job)