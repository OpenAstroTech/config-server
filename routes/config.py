from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

from models.build_config import BuildConfig


router = APIRouter(tags=["Configuration"])


class ConfigurationIn(BaseModel):
    approx_lat: float = Field(ge=-90, le=90, title="Approximate latitude of the pier")
    approx_lon: float = Field(
        ge=-180, le=180, title="Approximate longitude of the pier"
    )
    config_file: Optional[str] = Field(title="Local configuration file content")
    pio_env: Optional[str] = Field(title="PIO environment name")
    release_version: Optional[str] = Field()
    host_uuid: str = Field(title="Build host UUID")


@router.post("/")
async def upload_config(config: ConfigurationIn) -> BuildConfig:
    return await BuildConfig(**config.dict()).save()
