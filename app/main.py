import json
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request
from mongoengine import connect
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.attributes_helper import COMMON_ATTRIBUTES
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.span import SpanKind
from opencensus.trace.tracer import Tracer
from pydantic import BaseModel, Field

from app import models
from app.settings import *


class Configuration(BaseModel):
    approx_lat: float = Field()
    approx_lon: float = Field()
    config_file: Optional[str] = Field()
    pio_env: Optional[str] = Field()
    release_version: Optional[str] = Field()
    uuid: str = Field()


app = FastAPI()

db = connect(
    "configurations",
    host=settings.mongo_connection_string
)

exporter = None

if settings.appinsights_connection_string is not None:
    exporter = AzureExporter(connection_string=settings.appinsights_connection_string)
    sampler = ProbabilitySampler(1.0)


@app.middleware("http")
async def middleware_appinsights(request: Request, call_next):
    if exporter is None:
        return await call_next(request)

    tracer = Tracer(exporter=exporter, sampler=sampler)
    with tracer.span("main") as span:
        span.span_kind = SpanKind.SERVER

        response = await call_next(request)

        tracer.add_attribute_to_current_span(
            attribute_key=COMMON_ATTRIBUTES['HTTP_STATUS_CODE'],
            attribute_value=response.status_code)
        tracer.add_attribute_to_current_span(
            attribute_key=COMMON_ATTRIBUTES['HTTP_URL'],
            attribute_value=str(request.url))

    return response


@app.post("/config")
async def upload_config(config: Configuration):
    doc = models.Configuration(**config.dict()).save()
    return json.loads(doc.to_json())


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
