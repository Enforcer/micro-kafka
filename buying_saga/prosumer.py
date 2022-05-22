from kafka.consumer.fetcher import ConsumerRecord
from kafka import KafkaConsumer, KafkaProducer

from main import BROKER_URL


topics = ["messages"]
consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=BROKER_URL,
    group_id="saga",
)
producer = KafkaProducer(bootstrap_servers=BROKER_URL)

print("Consuming...")
for message in consumer:
    message: ConsumerRecord
    print(message)
    data = message.value.decode()
    try:
        pass
    except Exception:
        pass
        # if anything goes south, push to deadletter!
        # producer.send("messages_deadletter", value=b'some value')
