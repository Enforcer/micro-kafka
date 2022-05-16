from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers="localhost:9092", acks="all")

future = producer.send('foobar', value=b'some_message_bytesddd')
sent = future.get(timeout=30)  # wait until it's sent
print(sent)

