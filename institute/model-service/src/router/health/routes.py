from fastapi import APIRouter, status

from schemas.health import HealthCheck

router = APIRouter(prefix="/health")

tags = ["health"]

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
    tags=tags
)
@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
    tags=tags
)
async def health():
    return HealthCheck()
