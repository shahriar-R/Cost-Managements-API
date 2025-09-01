from fastapi import Request, HTTPException, status, Depends
from auth.tokens import TokenService
from auth.repositories import UserRepository
from auth.security import PasswordHasher
from auth.services import ACCESS_COOKIE

password_hasher = PasswordHasher()
user_repo = UserRepository(password_hasher)
token_service = TokenService()


def get_current_user(request: Request):
    token = request.cookies.get(ACCESS_COOKIE)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token"
        )

    try:
        payload = token_service.decode_token(token)
        if payload.type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
            )

        user = user_repo.get_by_username(payload.sub)
        if not user or user.token_version != payload.tv:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked"
            )

        return user.username
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )
