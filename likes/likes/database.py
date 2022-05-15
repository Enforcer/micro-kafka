from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    pass


def init_engine(db_uri: str) -> Engine:
    from likes.models import Like  # for models discovery

    engine = create_engine(db_uri, echo=True)
    Base.metadata.create_all(bind=engine)  # in prod use migrations
    return engine
