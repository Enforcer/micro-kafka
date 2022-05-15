from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from products.api.auth import UserId, get_current_user_id
from products.api.session_provider import get_session
from products.models import Product, ProductPhoto

api = APIRouter()


class PricePayload(BaseModel):
    amount: float
    currency: str


class ProductPayload(BaseModel):
    title: str
    short_description: str
    photos: list[str]
    price: PricePayload


@api.post("/products")
def create_product(
    payload: ProductPayload,
    user_id: UserId = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> Response:
    product = Product(
        seller_id=user_id,
        title=payload.title,
        short_description=payload.short_description,
        price=payload.price.amount,
        price_currency=payload.price.currency,
    )
    session.add(product)
    session.flush()
    for photo_url in payload.photos:
        photo = ProductPhoto(
            product_id=product.id,
            url=photo_url,
        )
        session.add(photo)

    return Response(status_code=201)


@api.get("/products")
def list_products(
    user_id: UserId = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> Response:
    own_products = session.query(Product).filter(Product.seller_id == user_id).all()
    serialized = [
        {
            "id": product.id,
            "title": product.title,
            "short_description": product.short_description,
            "photos": [photo.url for photo in product.photos],
            "price": {
                "amount": float(product.price),
                "currency": product.price_currency,
            },
        }
        for product in own_products
    ]

    return JSONResponse(content=serialized)


@api.post("/products/{product_id}/purchases")
def create_purchase(
    product_id: int,
    user_id: UserId = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> Response:
    product: Product | None = session.query(Product).get(product_id)
    if product is None:
        raise HTTPException(status_code=404)

    try:
        product.sell_to(user_id)
    except Product.SelfPurchase:
        raise HTTPException(status_code=422)
    except Product.AlreadySold:
        raise HTTPException(status_code=422)

    return JSONResponse(status_code=201)


class OfferPayload(BaseModel):
    price: PricePayload


@api.post("/products/{product_id}/offers")
def create_offer(
    product_id: int,
    offer: OfferPayload,
    user_id: UserId = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> Response:
    product: Product | None = session.query(Product).get(product_id)
    if product is None:
        raise HTTPException(status_code=404)

    try:
        product.offer_from(buyer_id=user_id, amount=offer.price.amount)
    except Product.ThatBuyerAlreadyHasOffer:
        raise HTTPException(status_code=422)

    return JSONResponse(status_code=201)


@api.get("/products/{product_id}/offers")
def get_offers(
    product_id: int,
    user_id: UserId = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> Response:
    product: Product | None = session.query(Product).get(product_id)
    if product is None:
        raise HTTPException(status_code=404)

    offers = product.offers_for(user_id)
    serialized = [
        {
            "id": offer.id,
            "price": {
                "amount": float(offer.price),
                "currency": offer.price_currency,
            },
        }
        for offer in offers
    ]

    return JSONResponse(serialized)


@api.delete("/products/{product_id}/offers/{offer_id}")
def withdraw_offer(
    product_id: int,
    offer_id: int,
    user_id: UserId = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> Response:
    product: Product | None = session.query(Product).get(product_id)
    if product is None:
        raise HTTPException(status_code=404)

    try:
        product.withdraw_offer(buyer_id=user_id, offer_id=offer_id)
    except Product.NoSuchOffer:
        raise HTTPException(status_code=404)

    return JSONResponse(status_code=204)


@api.post("/products/{product_id}/offers/{offer_id}/accept")
def accept_offer(
    product_id: int,
    offer_id: int,
    user_id: UserId = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> Response:
    product: Product | None = session.query(Product).get(product_id)
    if product is None:
        raise HTTPException(status_code=404)

    try:
        product.accept_offer(user_id=user_id, offer_id=offer_id)
    except Product.OnlyOwnerCanAcceptOffers:
        raise HTTPException(status_code=403)
    except Product.NoSuchOffer:
        raise HTTPException(status_code=404)

    return JSONResponse(status_code=200)
