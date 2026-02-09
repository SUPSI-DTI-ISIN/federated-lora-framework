from typing import Optional

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database import DatabaseConnector
from repositories.message import MessageRepository, MessageRepositoryInterface
from services.inference import InferenceServiceInterface, InferenceService
from services.message import MessageService, MessageServiceInterface

from clients.inference_service import InferenceServiceClientInterface, InferenceServiceClient
from config import settings

def get_inference_service_client() -> InferenceServiceClientInterface:
    return InferenceServiceClient.get_instance(inference_service_url=settings.inference_service_url)

def get_inference_service(inference_service_client: InferenceServiceClientInterface = Depends(get_inference_service_client)) -> InferenceServiceInterface:
    return InferenceService.get_instance(inference_service_client=inference_service_client)

def get_message_repository(db: AsyncSession = Depends(DatabaseConnector.get_db_session)) -> MessageRepositoryInterface:
    return MessageRepository(db_session=db)

def get_message_service(message_repository: MessageRepositoryInterface = Depends(get_message_repository), conversation_history_limit: Optional[int] = settings.conversation_history_limit) -> MessageServiceInterface:
    return MessageService(message_repository=message_repository, conversation_history_limit=conversation_history_limit)