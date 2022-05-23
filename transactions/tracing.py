from opentelemetry import trace
from opentelemetry.exporter.zipkin.proto.http import ZipkinExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.kafka import KafkaInstrumentor

THIS_SERVICE_NAME = ""
assert THIS_SERVICE_NAME, "Fill service name!"


resource = Resource(attributes={
    SERVICE_NAME: THIS_SERVICE_NAME
})

zipkin_exporter = ZipkinExporter(endpoint="http://localhost:9411/api/v2/spans")

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(zipkin_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

RequestsInstrumentor().instrument()
tracer = trace.get_tracer(__name__)
