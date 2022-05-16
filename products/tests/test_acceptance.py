import json
from typing import Any
from unittest.mock import Mock, patch

import pytest
from _pytest.tmpdir import TempPathFactory
from fastapi import FastAPI
from fastapi.testclient import TestClient
from tests.api_client import ApiClient

from products import producer
from products.api.app import create_app


@pytest.fixture(autouse=True)
def mock_producer():
    with patch.object(producer, "send") as send_patch:
        yield send_patch


def test_created_product_is_returned_on_list(api_client: ApiClient) -> None:
    create_response = api_client.create_product(user_id=1)
    assert create_response.status_code == 201

    get_response = api_client.get_products(user_id=1)
    assert get_response.status_code == 200
    assert get_response.json() == [
        {
            "id": 1,
            "title": "Brown Hat",
            "short_description": "Rarely used",
            "photos": [],
            "price": {
                "amount": 10.00,
                "currency": "PLN",
            },
        },
    ]


def test_created_product_sends_message(
    api_client: ApiClient, mock_producer: Mock
) -> None:
    create_response = api_client.create_product(user_id=1)
    assert create_response.status_code == 201

    assert mock_producer.called
    assert len(mock_producer.mock_calls) == 1
    the_only_call = mock_producer.mock_calls[0]
    assert the_only_call.args == ("products",)
    payload = json.loads(the_only_call.kwargs["value"].decode())
    assert payload == {
        "id": AnyInt(),
        "title": "Brown Hat",
        "short_description": "Rarely used",
        "price": 10.0,
        "price_currency": "PLN",
    }


def test_returns_only_own_products(api_client: ApiClient) -> None:
    create_response = api_client.create_product(user_id=1)
    assert create_response.status_code == 201

    get_response = api_client.get_products(user_id=2)
    assert get_response.status_code == 200


def test_purchase_returns_201(api_client: ApiClient) -> None:
    product_id = api_client.create_product_returning_id(user_id=1)

    purchase_response = api_client.purchase(user_id=2, product_id=product_id)
    assert purchase_response.status_code == 201


def test_cannot_purchase_purchased_product(api_client: ApiClient) -> None:
    product_id = api_client.create_product_returning_id(user_id=1)

    purchase_response_1 = api_client.purchase(user_id=2, product_id=product_id)
    assert purchase_response_1.status_code == 201

    purchase_response_2 = api_client.purchase(user_id=3, product_id=product_id)
    assert purchase_response_2.status_code == 422


def test_cannot_buy_own_product(api_client: ApiClient) -> None:
    product_id = api_client.create_product_returning_id(user_id=1)

    purchase_response = api_client.purchase(user_id=1, product_id=product_id)

    assert purchase_response.status_code == 422


def test_created_offer_is_returned_until_withdraw(api_client: ApiClient) -> None:
    product_id = api_client.create_product_returning_id(user_id=1)

    create_offer_response = api_client.offer(user_id=2, product_id=product_id)
    assert create_offer_response.status_code == 201

    get_offers_response = api_client.offers(user_id=2, product_id=product_id)
    assert get_offers_response.status_code == 200
    assert get_offers_response.json() == [
        {
            "id": 1,
            "price": {
                "amount": 5.0,
                "currency": "PLN",
            },
        }
    ]

    delete_offers_response = api_client.withdraw_offer(
        user_id=2, product_id=product_id, offer_id=1
    )
    assert delete_offers_response.status_code == 204

    get_offers_response = api_client.offers(user_id=2, product_id=product_id)
    assert get_offers_response.status_code == 200
    assert get_offers_response.json() == []


def test_cannot_create_two_offers_from_the_same_client(api_client: ApiClient) -> None:
    product_id = api_client.create_product_returning_id(user_id=1)

    create_offer_response = api_client.offer(user_id=2, product_id=product_id)
    assert create_offer_response.status_code == 201

    create_another_offer_response = api_client.offer(user_id=2, product_id=product_id)
    assert create_another_offer_response.status_code == 422


def test_seller_sees_all_offers_while_buyers_only_theirs(api_client: ApiClient) -> None:
    product_id = api_client.create_product_returning_id(user_id=1)

    create_offer_response = api_client.offer(
        user_id=2, product_id=product_id, price=6.0
    )
    assert create_offer_response.status_code == 201

    create_another_offer_response = api_client.offer(
        user_id=3, product_id=product_id, price=4.0
    )
    assert create_another_offer_response.status_code == 201

    seller_get_offers_response = api_client.offers(user_id=1, product_id=product_id)
    assert seller_get_offers_response.status_code == 200
    assert seller_get_offers_response.json() == [
        {
            "id": AnyInt(),
            "price": {
                "amount": 6.0,
                "currency": "PLN",
            },
        },
        {
            "id": AnyInt(),
            "price": {
                "amount": 4.0,
                "currency": "PLN",
            },
        },
    ]
    buyer_one_get_offers_response = api_client.offers(user_id=2, product_id=product_id)
    assert buyer_one_get_offers_response.status_code == 200
    assert buyer_one_get_offers_response.json() == [
        {
            "id": AnyInt(),
            "price": {
                "amount": 6.0,
                "currency": "PLN",
            },
        },
    ]

    buyer_two_get_offers_response = api_client.offers(user_id=3, product_id=product_id)
    assert buyer_two_get_offers_response.status_code == 200
    assert buyer_two_get_offers_response.json() == [
        {
            "id": AnyInt(),
            "price": {
                "amount": 4.0,
                "currency": "PLN",
            },
        }
    ]


def test_accepting_offer_changes_price_and_blocks_purchase_now_for_others(
    api_client: ApiClient,
) -> None:
    product_id = api_client.create_product_returning_id(user_id=1)

    create_offer_response = api_client.offer(
        user_id=2, product_id=product_id, price=5.0
    )
    assert create_offer_response.status_code == 201

    seller_get_offers_response = api_client.offers(user_id=1, product_id=product_id)
    assert seller_get_offers_response.status_code == 200
    first_offer = seller_get_offers_response.json()[0]
    first_offer_id = first_offer["id"]

    accept_response = api_client.accept_offer(
        user_id=1, product_id=product_id, offer_id=first_offer_id
    )
    assert accept_response.status_code == 200
    get_response = api_client.get_products(user_id=1)
    product = [
        product for product in get_response.json() if product["id"] == product_id
    ][0]
    assert product["price"] == {
        "amount": 5.0,
        "currency": "PLN",
    }

    purchase_response = api_client.purchase(user_id=3, product_id=product_id)
    assert purchase_response.status_code == 422


def test_only_product_owner_can_accept_offer(api_client: ApiClient) -> None:
    product_id = api_client.create_product_returning_id(user_id=1)

    create_offer_response = api_client.offer(
        user_id=2, product_id=product_id, price=5.0
    )
    assert create_offer_response.status_code == 201

    seller_get_offers_response = api_client.offers(user_id=1, product_id=product_id)
    assert seller_get_offers_response.status_code == 200
    first_offer = seller_get_offers_response.json()[0]
    first_offer_id = first_offer["id"]

    accept_response = api_client.accept_offer(
        user_id=2, product_id=product_id, offer_id=first_offer_id
    )
    assert accept_response.status_code == 403


def test_user_not_owning_offer_cannot_withdraw_it(api_client: ApiClient) -> None:
    product_id = api_client.create_product_returning_id(user_id=1)
    create_offer_response = api_client.offer(
        user_id=2, product_id=product_id, price=5.0
    )
    assert create_offer_response.status_code == 201
    seller_get_offers_response = api_client.offers(user_id=1, product_id=product_id)
    assert seller_get_offers_response.status_code == 200
    first_offer = seller_get_offers_response.json()[0]
    first_offer_id = first_offer["id"]

    withdraw_response = api_client.withdraw_offer(
        user_id=3, product_id=1, offer_id=first_offer_id
    )
    assert withdraw_response.status_code == 404


@pytest.fixture()
def api_client(client: TestClient) -> ApiClient:
    return ApiClient(client)


@pytest.fixture()
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def app(tmp_path_factory: TempPathFactory) -> FastAPI:
    tmp_path = tmp_path_factory.mktemp("test_db")
    test_db_path = tmp_path / "test_products.db"
    return create_app(f"sqlite:///{test_db_path}")


class AnyInt(int):
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, int):
            return super().__eq__(other)
        else:
            return True

    def __repr__(self) -> str:
        return "<any integer>"
