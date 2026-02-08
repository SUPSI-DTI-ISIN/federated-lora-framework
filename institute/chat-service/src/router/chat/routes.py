from typing import List

from fastapi import APIRouter, status, Depends
from shared_auth_library.entities import User

from auth import jwt_validator

from schemas.chat import ChatDTO
from schemas.chat.chat_creation_request_dto import ChatCreationRequestDTO
from services.chat import ChatServiceInterface
from .dependencies import get_chat_service

router = APIRouter(prefix="/chats")

tags = ["chat"]

@router.post(
    "/",
    response_model=ChatDTO,
    status_code=status.HTTP_201_CREATED,
    tags=tags
)
async def create_chat(
        chat_creation_request_dto: ChatCreationRequestDTO,
        chat_service: ChatServiceInterface = Depends(get_chat_service),
        user: User = Depends(jwt_validator.get_current_user_required)
):
    return await chat_service.create_new_chat(chat_creation_request_dto=chat_creation_request_dto, user_id=user.id)


@router.get(
    "",
    response_model=List[ChatDTO],
    status_code=status.HTTP_200_OK,
    tags=tags
)
async def list_chats(
        chat_service: ChatServiceInterface = Depends(get_chat_service),
        user: User = Depends(jwt_validator.get_current_user_required)
):
    return await chat_service.get_all_by_user(user_id=user.id)

@router.get(
    "/{chat_id}",
    response_model=ChatDTO,
    status_code=status.HTTP_200_OK,
    tags=tags
)
async def get_chat_by_id(
        chat_id: int,
        chat_service: ChatServiceInterface = Depends(get_chat_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    return await chat_service.get_by_id(chat_id=chat_id)

@router.delete(
    "/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=tags
)
async def delete_chat(
        chat_id: int,
        chat_service: ChatServiceInterface = Depends(get_chat_service),
        _: User = Depends(jwt_validator.get_current_user_required)
):
    await chat_service.delete_chat_by_user(chat_id=chat_id)