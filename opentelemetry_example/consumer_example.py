from time import sleep

from kafka import KafkaConsumer
from tracing import KafkaInstrumentor


consumer = KafkaConsumer(
    "foobar666",
    bootstrap_servers="localhost:9092",
)
KafkaInstrumentor().instrument()

for message in consumer:
    print(f"Got {message}")
    sleep(.2)
