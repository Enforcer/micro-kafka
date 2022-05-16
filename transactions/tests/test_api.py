import pytest
from _pytest.tmpdir import TempPathFactory
from fastapi import FastAPI
from fastapi.testclient import TestClient

from transactions.api import create_app


def test_balance_of_new_wallet(client: TestClient) -> None:
    response = client.get("/wallets/1")

    assert response.status_code == 200
    assert response.json() == {
        "balance": 0,
    }


def test_balance_of_credited_wallet_is_equal_to_credit(client: TestClient) -> None:
    response = client.post("/wallets/1/credit", json={"amount": 100})
    assert response.status_code == 204

    response = client.get("/wallets/1")

    assert response.status_code == 200
    assert response.json() == {
        "balance": 100,
    }


def test_debiting_wallet_lowers_balance(client: TestClient) -> None:
    response = client.post("/wallets/2/credit", json={"amount": 100})
    assert response.status_code == 204

    response = client.post("/wallets/2/debit", json={"amount": 33})
    assert response.status_code == 204

    response = client.get("/wallets/2")
    assert response.status_code == 200
    assert response.json() == {
        "balance": 67,
    }


@pytest.fixture()
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def app(tmp_path_factory: TempPathFactory) -> FastAPI:
    tmp_path = tmp_path_factory.mktemp("test_db")
    test_db_path = tmp_path / "test_transactions.db"
    return create_app(f"sqlite:///{test_db_path}")
