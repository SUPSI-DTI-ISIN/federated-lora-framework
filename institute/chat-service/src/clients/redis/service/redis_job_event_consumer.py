import redis.asyncio

from .redis_job_event_consumer_interface import RedisJobEventConsumerInterface
from commons import RedisChannel
from config import settings
from database import DatabaseConnector
from entities import MessageRole
from repositories.message import MessageRepository, MessageRepositoryInterface
from repositories.chat import ChatRepository, ChatRepositoryInterface
from schemas.celery import CeleryJobDTO, CeleryJobResultType
from schemas.message import MessageCreationRequestDTO
from services.chat import ChatService, ChatServiceInterface
from services.message import MessageService, MessageServiceInterface


class RedisJobEventConsumer(RedisJobEventConsumerInterface):
    def __init__(self, redis_client_async: redis.asyncio.Redis):
        self.__redis_client_async = redis_client_async

    async def start(self):
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

                    if celery_job_dto.result_type == CeleryJobResultType.FAILURE:
                        print("Inference task %s failed: %s", celery_job_dto.job_id, celery_job_dto.error)
                        continue

                    async with DatabaseConnector.get_session_factory()() as session:
                        chat_repository: ChatRepositoryInterface = ChatRepository(db_session=session)
                        message_repository: MessageRepositoryInterface = MessageRepository(db_session=session)
                        chat_service: ChatServiceInterface = ChatService(chat_repository=chat_repository)
                        message_service: MessageServiceInterface = MessageService(message_repository=message_repository, conversation_history_limit=settings.conversation_history_limit)

                        await chat_service.update_chat_inference_state(chat_id=celery_job_dto.result.chat_id, is_doing_inference=False)

                        assistant_message = MessageCreationRequestDTO(
                            chat_id=celery_job_dto.result.chat_id,
                            role=MessageRole.ASSISTANT,
                            content=celery_job_dto.result.response,
                            model_key=celery_job_dto.result.model_key,
                            adapter_version=celery_job_dto.result.adapter_version
                        )

                        await chat_service.update_chat_modification_date(chat_id=celery_job_dto.result.chat_id)

                        await message_service.create_new_message(message_creation_request_dto=assistant_message)

                except Exception as e:
                    print(f"Failed to process inference message: {e}")
        finally:
            await pubsub.punsubscribe(f"{RedisChannel.INFERENCE_RESULT.value}:*")
            await pubsub.close()