from fastapi import APIRouter, Depends, FastAPI, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from transactions.database import init_engine
from transactions.models import Wallet
from transactions.session_provider import get_session

api = APIRouter()


@api.get("/wallets/{user_id}")
def stats(user_id: int, session: Session = Depends(get_session)) -> Response:
    wallet = session.query(Wallet).get(user_id)
    if wallet is None:
        return JSONResponse({"balance": 0})
    else:
        return JSONResponse({"balance": wallet.balance})


class CreditDebitPayload(BaseModel):
    amount: int


@api.post("/wallets/{user_id}/credit")
def credit(user_id: int, payload: CreditDebitPayload, session: Session = Depends(get_session)) -> Response:
    wallet = session.query(Wallet).get(user_id)
    if wallet is None:
        new_wallet = Wallet(user_id=user_id, balance=payload.amount)
        session.add(new_wallet)
    else:
        wallet.balance += payload.amount

    return Response(status_code=204)


@api.post("/wallets/{user_id}/debit")
def debit(user_id: int, payload: CreditDebitPayload, session: Session = Depends(get_session)) -> Response:
    wallet = session.query(Wallet).get(user_id)
    if wallet is None:
        return JSONResponse({"error": "Not enough funds!"}, status_code=422)
    else:
        if wallet.balance < payload.amount:
            return JSONResponse({"error": "Not enough funds!"}, status_code=422)
        else:
            wallet.balance -= payload.amount

    return Response(status_code=204)


def create_app(database_uri: str) -> FastAPI:
    app = FastAPI()
    app.include_router(api)
    app.state.engine = init_engine(database_uri)
    return app
