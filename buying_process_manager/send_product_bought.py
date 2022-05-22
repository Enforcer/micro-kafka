import json

from kafka import KafkaProducer
from main import BROKER_URL

producer = KafkaProducer(bootstrap_servers=BROKER_URL)


payload = {
    "product_id": 1,
    "price": {
        "amount": 10.99,
        "currency": "PLN",
    },
}
serialized = json.dumps(payload).encode()


future = producer.send("products", value=serialized)
future.get(timeout=5)
