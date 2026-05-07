from typing import List

from clients.inference_service import InferenceServiceClientInterface
from clients.schemas import QueryRequestDTO, QueryResponseDTO
from schemas.chat import ConversationDTO
from schemas.exceptions import InferenceRequestError
from schemas.message import MessageDTO
from .inference_service_interface import InferenceServiceInterface

class InferenceService(InferenceServiceInterface):
    __INSTANCE = None

    def __init__(self, inference_service_client: InferenceServiceClientInterface):
        self.__inference_service_client = inference_service_client

    @classmethod
    def get_instance(cls, inference_service_client: InferenceServiceClientInterface):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(inference_service_client=inference_service_client)
        return cls.__INSTANCE

    async def inference_model(self, user_id: str, chat_id: int, user_message: MessageDTO, conversation_history: List[ConversationDTO]) -> bool:
        query_request_dto = QueryRequestDTO(
            user_id=user_id,
            chat_id=chat_id,
            model_key=user_message.model_key,
            adapter_version=user_message.adapter_version,
            prompt=user_message.content,
            conversation_history=conversation_history
        )

        try:
            await self.__inference_service_client.inference_model(query_request_dto=query_request_dto)
        except RuntimeError as err:
            raise InferenceRequestError(detailed_err=str(err))

        return True