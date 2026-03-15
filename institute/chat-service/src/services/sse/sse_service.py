import asyncio
from typing import Optional

import redis.asyncio
from sse_starlette import ServerSentEvent
from starlette.requests import Request

from commons import RedisChannel
from entities import MessageRole
from repositories.message import MessageRepositoryInterface
from schemas.celery import CeleryJobDTO, CeleryJobResultType
from schemas.message import MessageDTO
from schemas.sse import SseEvent
from services.sse import SseServiceInterface


class SseService(SseServiceInterface):
    __INSTANCE = None

    def __init__(self, redis_client_async: redis.asyncio.Redis, message_repository: MessageRepositoryInterface, poll_max_attempts: int, poll_interval: int):
        self.__redis_client_async = redis_client_async
        self.__message_repository = message_repository
        self.__poll_max_attempts = poll_max_attempts
        self.__poll_interval = poll_interval

    @classmethod
    def get_instance(cls, redis_client_async: redis.asyncio.Redis, message_repository: MessageRepositoryInterface, poll_max_attempts: int = 5, poll_interval: int = 0.5):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(redis_client_async=redis_client_async, message_repository=message_repository, poll_max_attempts=poll_max_attempts, poll_interval=poll_interval)
        return cls.__INSTANCE


    async def generate_sse_events(self, request: Request, user_id: str):
        pubsub = self.__redis_client_async.pubsub()

        await pubsub.subscribe(f"{RedisChannel.INFERENCE_RESULT.value}:{user_id}")

        try:
            while True:
                if await request.is_disconnected():
                    break

                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)

                if message is not None:
                    celery_job_dto = CeleryJobDTO.model_validate_json(message['data'])

                    if celery_job_dto.result_type == CeleryJobResultType.FAILURE:
                        yield ServerSentEvent(
                            data=celery_job_dto.model_dump_json(),
                            event=SseEvent.INFERENCE_JOB_FAILURE.value,
                        )
                    else:
                        assistant_message = await self.__poll_assistant_message(
                            chat_id=celery_job_dto.result.chat_id
                        )

                        if assistant_message is None:
                            yield ServerSentEvent(
                                data=celery_job_dto.model_dump_json(),
                                event=SseEvent.INFERENCE_JOB_FAILURE.value,
                            )
                        else:
                            yield ServerSentEvent(
                                data=assistant_message.model_dump_json(),
                                event=SseEvent.INFERENCE_JOB_SUCCESS.value,
                            )
                await asyncio.sleep(0.1)
        finally:
            await pubsub.unsubscribe(f"{RedisChannel.INFERENCE_RESULT.value}:{user_id}")
            await pubsub.close()


    async def __poll_assistant_message(self, chat_id: int) -> Optional[MessageDTO]:
        for attempt in range(self.__poll_max_attempts):
            latest = await self.__message_repository.get_latest_by_chat(chat_id=chat_id)

            if latest is not None and latest.role == MessageRole.ASSISTANT:
                return MessageDTO.model_validate(latest)
            await asyncio.sleep(self.__poll_interval)

        return None