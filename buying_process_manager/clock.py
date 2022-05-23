import time
from contextlib import contextmanager

from kafka import KafkaProducer
from main import BROKER_URL, DB_URI
from process_manager.database import init_engine
from process_manager.models import ProcessManager
from sqlalchemy.orm import Session

engine = init_engine(DB_URI)


producer = KafkaProducer(bootstrap_servers=BROKER_URL)


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


NUMBER_OF_SECONDS = 3600

while True:
    # ...
    time.sleep(NUMBER_OF_SECONDS)
