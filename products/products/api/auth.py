from fastapi import Depends
from fastapi.security import HTTPBearer

UserId = int


def get_current_user_id(auth=Depends(HTTPBearer())) -> UserId:
    return int(auth.credentials)
