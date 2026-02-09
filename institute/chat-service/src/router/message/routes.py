from typing import List

from fastapi import APIRouter, status, Depends
from shared_auth_library.entities import User

from auth import jwt_validator
from entities import MessageRole
from schemas.chat import ConversationDTO

from schemas.message import MessageDTO, InferenceRequestDTO, MessageCreationRequestDTO
from services.chat import ChatServiceInterface
from services.inference import InferenceServiceInterface
from services.message import MessageServiceInterface
from .dependencies import get_message_service, get_inference_service
import router.chat.dependencies as chat_dependencies

router = APIRouter(prefix="/chat/{chat_id}/messages")

tags = ["messages"]

@router.post(
    "",
    response_model=MessageDTO,
    status_code=status.HTTP_201_CREATED,
    tags=tags
)
async def send_message(
        chat_id: int,
        inference_request_dto: InferenceRequestDTO,
        message_service: MessageServiceInterface = Depends(get_message_service),
        inference_service: InferenceServiceInterface = Depends(get_inference_service),
        chat_service: ChatServiceInterface = Depends(chat_dependencies.get_chat_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    user_message = MessageCreationRequestDTO(
        chat_id=chat_id,
        role=MessageRole.USER,
        content=inference_request_dto.prompt,
        model_key=inference_request_dto.model_key,
        adapter_version=inference_request_dto.adapter_version
    )

    user_message_created = await message_service.create_new_message(message_creation_request_dto=user_message)

    chat_messages = await message_service.get_all_by_chat(chat_id=chat_id)

    conversation_history = [
        ConversationDTO(role=message.role, content=message.content)
        for message in reversed(chat_messages[:-1])
    ]

    inference_response_dto = await inference_service.inference_model(user_message=user_message_created, conversation_history=conversation_history)

    assistant_message = MessageCreationRequestDTO(
        chat_id=chat_id,
        role=MessageRole.ASSISTANT,
        content=inference_response_dto.response,
        model_key=inference_request_dto.model_key,
        adapter_version=inference_request_dto.adapter_version
    )

    assistant_message_created = await message_service.create_new_message(message_creation_request_dto=assistant_message)

    await chat_service.update_chat_modification_date(chat_id=chat_id)

    return assistant_message_created

@router.get(
    "",
    response_model=List[MessageDTO],
    status_code=status.HTTP_200_OK,
    tags=tags
)
async def get_messages(
        chat_id: int,
        message_service: MessageServiceInterface = Depends(get_message_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    return await message_service.get_all_by_chat(chat_id=chat_id)