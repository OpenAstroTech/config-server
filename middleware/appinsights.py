from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
from opencensus.trace.attributes_helper import COMMON_ATTRIBUTES
from opencensus.trace.span import SpanKind

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    DispatchFunction,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.types import ASGIApp

from settings import AppSettings


class AppInsightsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, dispatch: DispatchFunction | None = None) -> None:
        settings = AppSettings()
        if settings.appinsights_connection_string:
            exporter = AzureExporter(
                connection_string=AppSettings().appinsights_connection_string
            )
            sampler = ProbabilitySampler(1.0)

            self.tracer = Tracer(exporter=exporter, sampler=sampler)
        else:
            self.tracer = None
        super().__init__(app, dispatch)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        response = await call_next(request)

        if self.tracer is not None:
            with self.tracer.span("main") as span:
                span.span_kind = SpanKind.SERVER

            self.tracer.add_attribute_to_current_span(
                attribute_key=COMMON_ATTRIBUTES["HTTP_STATUS_CODE"],
                attribute_value=response.status_code,
            )
            self.tracer.add_attribute_to_current_span(
                attribute_key=COMMON_ATTRIBUTES["HTTP_URL"],
                attribute_value=str(request.url),
            )

        return response
