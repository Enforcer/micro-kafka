from fastapi import HTTPException, Request
from sqlalchemy.orm import Session


def get_session(request: Request) -> Session:
    engine = request.app.state.engine
    session = Session(bind=engine)
    request.state.session = session
    session.begin()
    try:
        yield session
    except HTTPException:
        session.rollback()
    else:
        session.commit()
    finally:
        session.close()
