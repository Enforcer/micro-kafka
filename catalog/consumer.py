from kafka.consumer.fetcher import ConsumerRecord
from sqlalchemy.orm import Session
from kafka import KafkaConsumer

from main import DB_URI, BROKER_URL
from contextlib import contextmanager
from catalog.database import init_engine

engine = init_engine(DB_URI)


@contextmanager
def session() -> Session:
    local_session = Session(bind=engine)
    local_session.begin()
    try:
        yield local_session
    except Exception:
        local_session.rollback()
        raise
    else:
        local_session.commit()
    finally:
        local_session.close()


topics = ['foobar']
consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=BROKER_URL,
    group_id="catalog",
)

print("Consuming...")
for message in consumer:
    message: ConsumerRecord
    print(message)
    data = message.value.decode()
    with session() as current_session:
        pass
