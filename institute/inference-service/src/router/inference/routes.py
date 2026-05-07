from fastapi import APIRouter, status, Depends

from schemas.inference import QueryRequestDTO
from services.inference import InferenceServiceInterface, get_inference_service

router = APIRouter(prefix="/inference")

tags = ["inference"]

@router.post(
    "",
    status_code=status.HTTP_202_ACCEPTED,
    tags=tags
)
async def query(
        query_request_dto: QueryRequestDTO,
        inference_service: InferenceServiceInterface = Depends(get_inference_service),
):
    await inference_service.inference_model(query_request_dto=query_request_dto)