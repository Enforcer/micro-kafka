import json
import traceback
from kafka.consumer.fetcher import ConsumerRecord
from kafka import KafkaConsumer, KafkaProducer
from threading import Timer

from main import BROKER_URL


topics = ["transactions_requests"]
consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=BROKER_URL,
    group_id="transactions",
)
producer = KafkaProducer(bootstrap_servers=BROKER_URL)


used_transaction_ids = set()


for message in consumer:
    message: ConsumerRecord
    print(f"Received: {message}")
    data = message.value.decode()
    try:
        decoded = json.loads(data)
        transaction_id = decoded["transaction_id"]
        if transaction_id in used_transaction_ids:
            print("Duplicated transaction ID! Ignoring...")
            continue
        else:
            used_transaction_ids.add(transaction_id)

        def callback():
            payload = {
                "transaction_id": transaction_id,
                "status": "OK",
            }
            data = json.dumps(payload).encode()
            producer.send("transactions_responses", value=data)

        timer = Timer(5.0, callback)
        timer.start()
    except Exception:
        print("Error!")
        traceback.print_exc()
