import os
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

SERVICE_NAME = os.getenv("SERVICE_NAME", "tp2-flask-app")
OTLP_ENDPOINT = os.getenv("OTLP_ENDPOINT", "http://otel-collector:4318")

resource = Resource.create({"service.name": SERVICE_NAME})

# Traces
trace_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(trace_provider)
span_exporter = OTLPSpanExporter(endpoint=f"{OTLP_ENDPOINT}/v1/traces")
trace_provider.add_span_processor(BatchSpanProcessor(span_exporter))

# Metrics
metric_exporter = OTLPMetricExporter(endpoint=f"{OTLP_ENDPOINT}/v1/metrics")
metric_reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=5000)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)