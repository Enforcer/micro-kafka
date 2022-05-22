from datetime import timedelta
from time import sleep
from kafka.consumer.fetcher import ConsumerRecord
from kafka import KafkaConsumer, KafkaProducer

from main import BROKER_URL


topics = ["messages_deadletter"]
consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=BROKER_URL,
    group_id="saga",
)
producer = KafkaProducer(bootstrap_servers=BROKER_URL)


def republish():
    messages = consumer.poll(max_records=100)
    for message in messages:
        message: ConsumerRecord
        print(message)
        data = message.value.decode()
        # if time come, republish message to "messages"
        #   producer.send("messages", value=b'some value')
        # otherwise, publish it back to the same topic (messages_deadletter)


RUN_EVERY = timedelta(minutes=30)


while True:
    republish()
    sleep(RUN_EVERY.total_seconds())
