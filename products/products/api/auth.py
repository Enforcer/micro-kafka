from fastapi import HTTPException, Request

UserId = int


def get_current_user_id(request: Request) -> int:
    try:
        user_id = request.headers["X-Authorized-User-Id"]
    except KeyError:
        raise HTTPException(status_code=401)
    return int(user_id)
