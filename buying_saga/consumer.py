import requests
from kafka.consumer.fetcher import ConsumerRecord
from kafka import KafkaConsumer, KafkaProducer

from main import BROKER_URL


topics = ['foobar']
consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=BROKER_URL,
    group_id="catalog",
)
producer = KafkaProducer(bootstrap_servers=BROKER_URL)

print("Consuming...")
for message in consumer:
    message: ConsumerRecord
    print(message)
    data = message.value.decode()
    # producer.send('foobar', value=b'some value')
    # requests.post()
