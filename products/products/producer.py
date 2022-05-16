from kafka import KafkaProducer
from main import BROKER_URL

producer: KafkaProducer | None = None


def send(topic: str, value: bytes) -> None:
    global producer
    if producer is None:  # lazy evaluation
        producer = KafkaProducer(bootstrap_servers=BROKER_URL)

    producer.send(topic, value=value)
