import redis.asyncio
import asyncio

from clients.redis.service.redis_job_event_consumer_interface import RedisJobEventConsumerInterface
from commons import RedisChannel
from schemas.celery import CeleryJobDTO
from services.federated_learning_job import FederatedLearningJobServiceInterface


class RedisJobEventConsumer(RedisJobEventConsumerInterface):
    __INSTANCE = None

    def __init__(self, redis_client_async: redis.asyncio.Redis, federated_learning_job_service: FederatedLearningJobServiceInterface):
        self.__redis_client_async = redis_client_async
        self.__federated_learning_job_service = federated_learning_job_service

    @classmethod
    def get_instance(cls, redis_client_async: redis.asyncio.Redis, federated_learning_job_service: FederatedLearningJobServiceInterface):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(redis_client_async=redis_client_async, federated_learning_job_service=federated_learning_job_service)
        return cls.__INSTANCE

    async def start(self):
        pubsub = self.__redis_client_async.pubsub()

        await pubsub.subscribe(RedisChannel.JOB_UPDATES.value)

        try:
            while True:
                message = await pubsub.get_message(
                    ignore_subscribe_messages=True,
                    timeout=1.0,
                )

                if message is None:
                    await asyncio.sleep(0.1)
                    continue

                celery_job_dto = CeleryJobDTO.model_validate_json(message["data"])

                await self.__federated_learning_job_service.update_job_status_from_celery(celery_job_dto=celery_job_dto)
        finally:
            await pubsub.unsubscribe(RedisChannel.JOB_UPDATES.value)
            await pubsub.close()