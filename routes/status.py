from enum import Enum
from fastapi import APIRouter, Response
from pydantic import BaseModel

router = APIRouter(tags=["Status"])


class HealthStatus(Enum):
    DOWN = 0
    UP = 1


class Health(BaseModel):
    api: HealthStatus


@router.get("/health")
async def health() -> Health:
    return Health(api=HealthStatus.UP)


@router.head("/health")
async def health_silent() -> Health:
    return Response(status_code=200)
