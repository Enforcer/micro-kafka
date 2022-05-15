from sqlalchemy import Column, Integer

from likes.database import Base


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer(), primary_key=True)
    product_id = Column(Integer(), nullable=False)
    user_id = Column(Integer(), nullable=False)
