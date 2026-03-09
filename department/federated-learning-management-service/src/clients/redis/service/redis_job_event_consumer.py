import redis.asyncio

from clients.redis.service.redis_job_event_consumer_interface import RedisJobEventConsumerInterface
from commons import RedisChannel
from database import DatabaseConnector
from repositories.federated_learning_job import FederatedLearningJobRepository
from schemas.celery import CeleryJobDTO
from services.federated_learning_job import FederatedLearningJobService


class RedisJobEventConsumer(RedisJobEventConsumerInterface):
    def __init__(self, redis_client_async: redis.asyncio.Redis):
        self.__redis_client_async = redis_client_async

    async def start(self):
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
                    async with DatabaseConnector.get_session_factory()() as session:
                        federated_learning_job_repository = FederatedLearningJobRepository(db_session=session)
                        federated_learning_job_service = FederatedLearningJobService(federated_learning_job_repository=federated_learning_job_repository)
                        await federated_learning_job_service.update_job_status_from_celery(celery_job_dto=celery_job_dto)
                except Exception as e:
                    print(f"Failed to process job update message: {e}")
        finally:
            await pubsub.unsubscribe(RedisChannel.JOB_UPDATES.value)
            await pubsub.close()