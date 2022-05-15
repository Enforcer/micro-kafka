from fastapi import APIRouter, Depends, FastAPI, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from likes.database import init_engine
from likes.models import Like
from likes.session_provider import get_session

api = APIRouter()


@api.get("/stats")
def stats(session: Session = Depends(get_session)) -> Response:
    total_likes = session.query(Like).count()
    return JSONResponse({"total_likes": total_likes})


def create_app(database_uri: str) -> FastAPI:
    app = FastAPI()
    app.include_router(api)
    app.state.engine = init_engine(database_uri)
    return app
