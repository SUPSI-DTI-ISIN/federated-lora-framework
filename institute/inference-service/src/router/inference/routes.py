from fastapi import APIRouter, status, Depends

from schemas.inference import QueryResponseDTO, QueryRequestDTO
from services.inference import InferenceServiceInterface
from services.model import ModelServiceInterface
from .dependencies import get_inference_service, get_model_service

router = APIRouter(prefix="/inference")

tags = ["inference"]

@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=QueryResponseDTO,
    tags=tags
)
async def query(
        query_request_dto: QueryRequestDTO,
        model_service: ModelServiceInterface = Depends(get_model_service),
        inference_service: InferenceServiceInterface = Depends(get_inference_service),
):
    loaded_model = model_service.get_or_load_model(model_key=query_request_dto.model_key, adapter_version=query_request_dto.adapter_version)

    return await inference_service.inference_model(query_request_dto=query_request_dto, loaded_model=loaded_model)