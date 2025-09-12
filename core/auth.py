from fastapi import HTTPException, Request
from datetime import datetime, timedelta


SECRET_KEY = "09d25e094faa6ca2566b7a9563b93f70aa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

fake_users_db = {"user": {"username": "user1", "password": "pass1"}}


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode["exp"] = datetime.timezone.utc() + expires_delta
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(username: str):
    return create_token(
        {"sub": username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(username: str):
    return create_token({"sub": username}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    username = verify_token(token)
    if username not in fake_users_db:
        raise HTTPException(status_code=401, detail="Invalid user")
    return username
