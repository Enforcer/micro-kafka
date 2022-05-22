from contextlib import contextmanager

from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
from main import BROKER_URL, DB_URI
from process_manager.database import init_engine
from process_manager.models import ProcessManager
from sqlalchemy.orm import Session

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


topics = ["products", "transactions_responses"]
consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=BROKER_URL,
    group_id="buying_process_manager",
)

for message in consumer:
    message: ConsumerRecord
    print(message)
    data = message.value.decode()
    with session() as current_session:
        # current_session.query(ProcessManager)
        pass
