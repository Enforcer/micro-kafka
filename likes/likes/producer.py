from kafka import KafkaProducer

from main import BROKER_URL

producer = KafkaProducer(bootstrap_servers=BROKER_URL)
