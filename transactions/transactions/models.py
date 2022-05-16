from sqlalchemy import Column, Integer, ForeignKey

from transactions.database import Base


class Wallet(Base):
    __tablename__ = "wallets"

    user_id = Column(Integer(), primary_key=True)
    balance = Column(Integer(), nullable=False)
