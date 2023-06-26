from typing import Optional
from beanie import Document
from pydantic import Field


class BuildConfig(Document):
    approx_lat: float = Field(ge=-90, le=90)
    approx_lon: float = Field(ge=-180, le=180)
    config_file: Optional[str] = None
    pio_env: Optional[str] = None
    release_version: Optional[str] = None
    host_uuid: str

    class Settings:
        name = "build_configs"
