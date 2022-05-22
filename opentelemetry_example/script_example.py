import requests
from opentelemetry.trace import Span

from tracing import tracer, RequestsInstrumentor


RequestsInstrumentor().instrument()


with tracer.start_as_current_span(name="Script2") as span:
    span: Span
    span.add_event("Example", {"count": 1})
    requests.get("http://localhost:8000/endpoint", headers={
        "trace_id": str(span.get_span_context().trace_id),
    })
