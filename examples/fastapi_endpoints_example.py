from decimal import Decimal
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# =*= Example #1 =*=
# Returning error status code
@app.get("/error")
def error():
    raise HTTPException(status_code=501)


# =*= Example #2 =*=
# Passing arguments
@app.get("/items/{item_id}")
def single_item(item_id):
    return {"id": item_id, "name": f"Item {item_id}"}


# =*= Example #3 =*=
# Creating new item & other HTTP methods
class Book(BaseModel):
    name: str
    price_amount: Decimal
    price_currency: str
    reviewer: Optional[str]


@app.post("/items")
def new_book(book: Book):
    print(f"Creating {book}")
    return {
        "id": 1,
        "name": book.name,
        "price": {"amount": book.price_amount, "currency": book.price_currency},
    }
