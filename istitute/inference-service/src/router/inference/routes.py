from fastapi import APIRouter, status, Depends

from schemas.inference import QueryResponseDTO
from schemas.inference.query_request_dto import QueryRequestDTO
from services import InferenceServiceInterface
from .dependencies import get_inference_service

router = APIRouter(prefix="/inference")

tags = ["inference"]

@router.post(
    "/query",
    status_code=status.HTTP_200_OK,
    response_model=QueryResponseDTO,
    tags=tags
)
async def query(query_request_dto: QueryRequestDTO, inference_service: InferenceServiceInterface = Depends(get_inference_service)):
    return await inference_service.inference_model(query_request_dto=query_request_dto)