import pytest
from _pytest.tmpdir import TempPathFactory
from fastapi import FastAPI
from fastapi.testclient import TestClient

from likes.api import create_app


def test_stats(client: TestClient) -> None:
    response = client.get("/stats")

    assert response.status_code == 200
    assert response.json() == {
        "total_likes": 0,
    }


@pytest.fixture()
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def app(tmp_path_factory: TempPathFactory) -> FastAPI:
    tmp_path = tmp_path_factory.mktemp("test_db")
    test_db_path = tmp_path / "test_likes.db"
    return create_app(f"sqlite:///{test_db_path}")
