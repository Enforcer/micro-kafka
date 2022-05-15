import asyncio
import random
from collections import Counter

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


PRICES = [
    "1.99",
    "5.99",
    "9.99",
    "19.99",
    "29.99",
    "39.99",
]


class Payload(BaseModel):
    title: str
    currency: str


class EstimateResult(BaseModel):
    estimated_price: float


@app.post("/estimate", response_model=EstimateResult)
async def estimate(payload: Payload) -> Response:
    if random.random() < 0.2:  # 20% of cases
        await asyncio.sleep(10)
    elif random.random() < 0.4:  # another 20% of cases
        raise HTTPException(status_code=503)

    formula = (
        len(payload.title)
        + Counter(payload.title.lower()).get("a", 0)
        + sum(ord(letter) for letter in payload.currency)
    )
    result = PRICES[formula % len(PRICES)]

    return JSONResponse({"estimated_price": result})
