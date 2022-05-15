from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from products.database import Base


class Product(Base):
    __tablename__ = "products"

    class SelfPurchase(Exception):
        pass

    class AlreadySold(Exception):
        pass

    class ThatBuyerAlreadyHasOffer(Exception):
        pass

    class NoSuchOffer(Exception):
        pass

    class OnlyOwnerCanAcceptOffers(Exception):
        pass

    id = Column(Integer(), primary_key=True)
    seller_id = Column(Integer(), nullable=False)
    title = Column(String(255), nullable=False)
    short_description = Column(String(255), nullable=False)
    price = Column(Numeric(), nullable=False)
    price_currency = Column(String(3), nullable=False)
    sold = Column(Boolean(), nullable=False, default=False)

    photos = relationship("ProductPhoto")
    offers = relationship("Offer", cascade="save-update, delete, delete-orphan")

    def sell_to(self, buyer_id: int) -> None:
        if buyer_id == self.seller_id:
            raise self.SelfPurchase

        if self.sold:
            raise self.AlreadySold

        self.sold = True

    def offer_from(self, buyer_id: int, amount: float) -> None:
        offer_from_the_same_buyer = [
            offer for offer in self.offers if offer.buyer_id == buyer_id
        ]
        if len(offer_from_the_same_buyer) > 0:
            raise self.ThatBuyerAlreadyHasOffer

        new_offer = Offer(
            buyer_id=buyer_id,
            price=amount,
            price_currency=self.price_currency,
        )
        self.offers.append(new_offer)

    def offers_for(self, user_id: int) -> list["Offer"]:
        if user_id == self.seller_id:
            return self.offers
        else:
            return [offer for offer in self.offers if offer.buyer_id == user_id]

    def withdraw_offer(self, buyer_id: int, offer_id: int) -> None:
        buyers_offers = [
            offer
            for offer in self.offers
            if offer.buyer_id == buyer_id and offer.id == offer_id
        ]
        if len(buyers_offers) == 0:
            raise self.NoSuchOffer

        self.offers.remove(buyers_offers[0])

    def accept_offer(self, user_id: int, offer_id: int) -> None:
        if user_id != self.seller_id:
            raise self.OnlyOwnerCanAcceptOffers

        the_offer = [offer for offer in self.offers if offer.id == offer_id]
        if len(the_offer) == 0:
            raise self.NoSuchOffer

        self.price = the_offer[0].price
        self.sold = True


class ProductPhoto(Base):
    __tablename__ = "photos"

    id = Column(Integer(), primary_key=True)
    product_id = Column(Integer(), ForeignKey("products.id"), nullable=False)
    url = Column(String(255), nullable=False)


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer(), primary_key=True)
    product_id = Column(Integer(), ForeignKey("products.id"), nullable=False)
    buyer_id = Column(Integer(), nullable=False)
    price = Column(Numeric(), nullable=False)
    price_currency = Column(String(3), nullable=False)
