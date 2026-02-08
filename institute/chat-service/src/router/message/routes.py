from typing import List

from fastapi import APIRouter, status, Depends
from shared_auth_library.entities import User

from auth import jwt_validator

from schemas.message import MessageDTO, InferenceRequestDTO
from services.message import MessageServiceInterface
from .dependencies import get_message_service

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
        user: User = Depends(jwt_validator.get_current_user_required)
):
    return "ok"
    """
    chat = db.query(models.Chat) \
        .filter(models.Chat.id == chat_id, models.Chat.user_id == current_user_id) \
        .first()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Save user message
    user_message = models.Message(
        chat_id=chat_id,
        role=models.MessageRole.USER,
        content=message.content
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # Get conversation history (last N messages)
    history = db.query(models.Message) \
        .filter(models.Message.chat_id == chat_id) \
        .order_by(models.Message.created_at.desc()) \
        .limit(10) \
        .all()

    conversation_history = [
        {"role": msg.role.value, "content": msg.content}
        for msg in reversed(history[:-1])  # Exclude the message we just added
    ]

    # Call inference service
    try:
        async with httpx.AsyncClient() as client:
            inference_request = schemas.InferenceRequest(
                chat_id=chat_id,
                user_message=message.content,
                conversation_history=conversation_history
            )

            response = await client.post(
                f"{INFERENCE_SERVICE_URL}/inference",
                json=inference_request.dict(),
                timeout=60.0
            )
            response.raise_for_status()
            inference_result = schemas.InferenceResponse(**response.json())

    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Inference service error: {str(e)}"
        )

    # Save AI response
    ai_message = models.Message(
        chat_id=chat_id,
        role=models.MessageRole.ASSISTANT,
        content=inference_result.response,
        tokens=inference_result.tokens_used,
        model_version=inference_result.model_version
    )
    db.add(ai_message)

    # Update chat timestamp
    chat.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(ai_message)

    return ai_message
    """

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