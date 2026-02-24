import asyncio

import redis.asyncio
from sse_starlette import ServerSentEvent
from starlette.requests import Request

from commons import RedisChannel
from schemas.job import FederatedLearningJobDTO
from schemas.sse import SseEvent
from services.sse.sse_service_interface import SseServiceInterface


class SseService(SseServiceInterface):
    __INSTANCE = None

    def __init__(self, redis_client_async: redis.asyncio.Redis):
        self.__redis_client_async = redis_client_async

    @classmethod
    def get_instance(cls, redis_client_async: redis.asyncio.Redis):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(redis_client_async=redis_client_async)
        return cls.__INSTANCE


    async def generate_sse_events(self, request: Request):
        pubsub = self.__redis_client_async.pubsub()

        await pubsub.subscribe(RedisChannel.JOB_UPDATES.value)

        try:
            while True:
                if await request.is_disconnected():
                    break

                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)

                if message is not None:
                    data = FederatedLearningJobDTO.model_validate_json(message['data'])

                    yield ServerSentEvent(
                        data=data.model_dump_json(),
                        event=SseEvent.FEDERATED_LEARNING_JOB_UPDATE.value,
                    )

                await asyncio.sleep(0.1)
        finally:
            await pubsub.unsubscribe(RedisChannel.JOB_UPDATES.value)
            await pubsub.close()