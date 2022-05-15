import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from catalog.api import create_app


def test_stats(client: TestClient) -> None:
    response = client.get("/stats")

    assert response.status_code == 200
    assert response.json() == {
        "total_products": 0,
    }


@pytest.fixture()
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def app(test_db_connection_uri: str) -> FastAPI:
    app = create_app(database_uri=test_db_connection_uri)
    yield app
    app.state.engine.dispose()  # close all connections so test DB can be removed


@pytest.fixture(scope="session")
def test_db_connection_uri() -> str:
    from main import DB_URI
    from sqlalchemy import create_engine, text

    regular_engine = create_engine(DB_URI)

    regular_db_name = regular_engine.url.database
    test_database_name = f"test_{regular_db_name}"

    with regular_engine.connect().execution_options(
        isolation_level="AUTOCOMMIT"
    ) as connection:
        connection.execute(text(f"DROP DATABASE IF EXISTS {test_database_name}"))
        connection.execute(text(f"CREATE DATABASE {test_database_name}"))

    new_url = regular_engine.url.set(database=test_database_name)
    yield new_url

    with regular_engine.connect().execution_options(
        isolation_level="AUTOCOMMIT"
    ) as connection:
        connection.execute(text(f"DROP DATABASE IF EXISTS {test_database_name}"))
