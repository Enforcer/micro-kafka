from kafka import KafkaProducer

from tracing import FastAPIInstrumentor, KafkaInstrumentor
from fastapi import FastAPI, Request

app = FastAPI()


producer = KafkaProducer(bootstrap_servers="localhost:9092")


@app.get("/endpoint")
def get(request: Request):
    print(request.headers)
    producer.send(topic="foobar666", value=b"value")
    # sleep(0.3)
    return {"ok": 1}


FastAPIInstrumentor().instrument_app(app)
KafkaInstrumentor().instrument()
