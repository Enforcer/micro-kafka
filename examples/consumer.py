from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord

consumer = KafkaConsumer(
    'foobar',
    bootstrap_servers="localhost:9092",
    enable_auto_commit=False,  # by default offsets are committed every 5 seconds
    group_id="testy",
)
for msg in consumer:
    msg: ConsumerRecord
    print(msg)
    # anonymous consumer and no commiting would cause the consumer to start
    # consuming from new messages of the topic
    consumer.commit()
