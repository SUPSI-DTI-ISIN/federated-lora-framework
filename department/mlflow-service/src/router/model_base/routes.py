from fastapi import APIRouter, status

from schemas.model_base import ModelBaseDTO

router = APIRouter(prefix="/model/base")

tags = ["model-base"]

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ModelBaseDTO,
    tags=tags
)
@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ModelBaseDTO,
    tags=tags
)
async def get_model_base_artifact_uri():
    return ModelBaseDTO(model_base_artifact_uri="test-uri")
