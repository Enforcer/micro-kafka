from contextlib import contextmanager

from kafka import KafkaProducer
from main import BROKER_URL, DB_URI
from sqlalchemy.orm import Session

from products.database import init_engine

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


def main() -> None:
    pass


if __name__ == "__main__":
    main()
