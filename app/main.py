import json

import uvicorn
from fastapi import FastAPI
from mongoengine import connect
from pydantic import BaseModel, Field, BaseSettings

from app import models


class AppSettings(BaseSettings):
    mongo_host: str
    mongo_port: int
    mongo_root_user: str
    mongo_root_password: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = AppSettings()


class Configuration(BaseModel):
    lat: float = Field()
    lon: float = Field()
    config_file: str = Field()
    pio_env: str = Field()
    release_version: str = Field()
    uuid: str = Field()


app = FastAPI()

db = connect(
    "oat",
    host=settings.mongo_host,
    port=settings.mongo_port,
    username=settings.mongo_root_user,
    password=settings.mongo_root_password
)


@app.post("/config")
async def upload_config(config: Configuration):
    doc = models.Configuration(**config.dict()).save()
    return json.loads(doc.to_json())


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
