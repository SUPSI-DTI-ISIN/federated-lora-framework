import redis.asyncio

from datetime import datetime, timezone

from commons import RedisChannel
from entities import MessageRole, MessageModel
from repositories.chat import build_chat_repository, ChatRepositoryInterface
from repositories.message import build_message_repository, MessageRepositoryInterface
from schemas.celery import CeleryJobResultType, CeleryJobDTO, QueryResponseDTO
from schemas.exceptions import ChatNotFoundError
from services.redis import RedisEventConsumerServiceInterface

from database import DatabaseConnector

class InferenceResultRedisEventConsumer(RedisEventConsumerServiceInterface):
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
        await pubsub.psubscribe(f"{RedisChannel.INFERENCE_RESULT.value}:*")
        try:
            async for message in pubsub.listen():
                if message is None:
                    continue
                if message.get("type") != "pmessage":
                    continue
                try:
                    celery_job_dto = CeleryJobDTO.model_validate_json(message["data"])

                    is_inference_failed = False

                    if celery_job_dto.result_type == CeleryJobResultType.FAILURE or celery_job_dto.result is None:
                        print("Inference task %s failed: %s", celery_job_dto.job_id, celery_job_dto.error)
                        is_inference_failed = True

                    await self.__handle_assistant_inference_message(is_inference_failed=is_inference_failed, celery_job_dto=celery_job_dto)

                except Exception as e:
                    print(f"Failed to process inference message: {e}")
        finally:
            await pubsub.punsubscribe(f"{RedisChannel.INFERENCE_RESULT.value}:*")
            await pubsub.close()

    async def __handle_assistant_inference_message(self, is_inference_failed: bool, celery_job_dto: CeleryJobDTO) -> None:
        if celery_job_dto is None:
            return

        async with DatabaseConnector.get_session_factory()() as session:
            chat_repository = build_chat_repository(db=session)
            message_repository = build_message_repository(db=session)

            await self.__update_chat_inference_state(chat_repository=chat_repository, chat_id=celery_job_dto.chat_id)
            await self.__update_chat_modification_date(chat_repository=chat_repository, chat_id=celery_job_dto.chat_id)

            if is_inference_failed or celery_job_dto.result is None:
                assistant_message = MessageModel(
                    chat_id=celery_job_dto.chat_id,
                    role=MessageRole.ASSISTANT,
                    content="Error during inference",
                    model_key=None,
                    adapter_version=None,
                    created_at=datetime.now(timezone.utc)
                )
            else:
                assistant_message = MessageModel(
                    chat_id=celery_job_dto.chat_id,
                    role=MessageRole.ASSISTANT,
                    content=celery_job_dto.result.response,
                    model_key=celery_job_dto.result.model_key,
                    adapter_version=celery_job_dto.result.adapter_version,
                    created_at=datetime.now(timezone.utc)
                )

            await self.__create_new_message(message_repository=message_repository, message_model=assistant_message)

    async def __update_chat_inference_state(self, chat_repository: ChatRepositoryInterface, chat_id: int):
        chat = await chat_repository.get_by_id(chat_id=chat_id)

        if chat is None:
            raise ChatNotFoundError(chat_id=chat_id)

        chat.is_doing_inference = False

        await chat_repository.save_chat(chat_model=chat)

    async def __update_chat_modification_date(self, chat_repository: ChatRepositoryInterface, chat_id: int):
        chat = await chat_repository.get_by_id(chat_id=chat_id)

        if chat is None:
            raise ChatNotFoundError(chat_id=chat_id)

        chat.updated_at = datetime.now(timezone.utc)

        await chat_repository.save_chat(chat_model=chat)

    async def __create_new_message(self, message_repository: MessageRepositoryInterface, message_model: MessageModel):
        await message_repository.save_message(message_model=message_model)