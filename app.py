from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi import FastAPI

from models.build_config import BuildConfig
from middleware.appinsights import AppInsightsMiddleware

from routes import config, status
from settings import AppSettings

app = FastAPI()


@app.on_event("startup")
async def start_db():
    await init_db()


async def init_db():
    client: AsyncIOMotorClient = AsyncIOMotorClient(
        AppSettings().mongo_connection_string
    )

    await init_beanie(database=client.oatconf, document_models=[BuildConfig])


v1 = FastAPI()

v1.add_middleware(middleware_class=AppInsightsMiddleware)

v1.include_router(router=status.router, prefix="/status")
v1.include_router(router=config.router, prefix="/config")

app.mount("/api/v1", v1)
