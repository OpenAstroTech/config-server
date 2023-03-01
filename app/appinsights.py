from fastapi import Request

from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.attributes_helper import COMMON_ATTRIBUTES
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.span import SpanKind
from opencensus.trace.tracer import Tracer

