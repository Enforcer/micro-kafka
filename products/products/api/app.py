from fastapi import FastAPI

from products.api.views import api
from products.database import init_engine


def create_app(database_uri: str) -> FastAPI:
    app = FastAPI()
    app.include_router(api)

    app.state.engine = init_engine(database_uri)

    return app
