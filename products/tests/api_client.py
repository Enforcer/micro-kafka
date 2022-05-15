from fastapi.testclient import TestClient
from requests import Response


class ApiClient:
    def __init__(self, client: TestClient) -> None:
        self._client = client

    def create_product(self, user_id: int) -> Response:
        return self._client.post(
            "/products",
            headers=self._auth_header_for(user_id=user_id),
            json={
                "title": "Brown Hat",
                "short_description": "Rarely used",
                "photos": [],
                "price": {
                    "amount": 10.00,
                    "currency": "PLN",
                },
            },
        )

    def create_product_returning_id(self, user_id: int) -> int:
        create_response = self.create_product(user_id=user_id)
        assert create_response.status_code == 201
        get_response = self._client.get(
            "/products", headers=self._auth_header_for(user_id)
        )
        last_product = get_response.json()[-1]
        return last_product["id"]

    def get_products(self, user_id: int) -> Response:
        return self._client.get("/products", headers=self._auth_header_for(user_id))

    def purchase(self, user_id: int, product_id: int) -> Response:
        return self._client.post(
            f"/products/{product_id}/purchases",
            headers=self._auth_header_for(user_id),
        )

    def offer(self, user_id: int, product_id: int, price: float = 5.0) -> Response:
        return self._client.post(
            f"/products/{product_id}/offers",
            headers=self._auth_header_for(user_id),
            json={
                "price": {
                    "amount": price,
                    "currency": "PLN",
                }
            },
        )

    def offers(self, user_id: int, product_id: int) -> Response:
        return self._client.get(
            f"/products/{product_id}/offers",
            headers=self._auth_header_for(user_id),
        )

    def withdraw_offer(self, user_id: int, product_id: int, offer_id: int) -> Response:
        return self._client.delete(
            f"/products/{product_id}/offers/{offer_id}",
            headers=self._auth_header_for(user_id),
        )

    def accept_offer(self, user_id: int, product_id: int, offer_id: int) -> Response:
        return self._client.post(
            f"/products/{product_id}/offers/{offer_id}/accept",
            headers=self._auth_header_for(user_id),
        )

    def _auth_header_for(self, user_id: int) -> dict:
        return {"X-Authorized-User-Id": str(user_id)}
