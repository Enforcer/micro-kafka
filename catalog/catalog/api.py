from fastapi import APIRouter, Depends, FastAPI, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from catalog.database import init_engine
from catalog.models import Product
from catalog.session_provider import get_session

api = APIRouter()


@api.get("/stats")
def stats(session: Session = Depends(get_session)) -> Response:
    total_products = session.query(Product).count()
    return JSONResponse({"total_products": total_products})


@api.get("/search/{term}")
def search(term: str, session: Session = Depends(get_session)) -> Response:
    products = session.query(Product).filter(Product.__ts_vector__.match(term)).limit(5)
    return JSONResponse([product.data for product in products])


def create_app(database_uri: str) -> FastAPI:
    app = FastAPI()
    app.include_router(api)
    app.state.engine = init_engine(database_uri)
    return app
