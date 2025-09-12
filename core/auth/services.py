import uuid
from fastapi import HTTPException, status, Response, Request
from app.auth.repositories import UserRepository
from app.auth.tokens import TokenService
from app.config import settings
from datetime import timedelta

ACCESS_COOKIE = "access_token"
REFRESH_COOKIE = "refresh_token"


class AuthService:
    def __init__(self, user_repo: UserRepository, token_service: TokenService):
        self.user_repo = user_repo
        self.token_service = token_service
        self.valid_refresh: dict[str, dict] = {}  # در عمل بهتره Redis باشه

    def login(self, username: str, password: str, response: Response):
        user = self.user_repo.verify_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        # ساخت توکن‌ها
        access = self.token_service.create_token(
            subject=user.username,
            ttl=settings.ACCESS_TOKEN_EXPIRE,
            token_type="access",
            token_version=user.token_version,
        )
        refresh_jti = str(uuid.uuid4())
        refresh = self.token_service.create_token(
            subject=user.username,
            ttl=settings.REFRESH_TOKEN_EXPIRE,
            token_type="refresh",
            token_version=user.token_version,
            jti=refresh_jti,
        )
        self.valid_refresh[refresh_jti] = {"sub": user.username}

        self._set_cookie(response, ACCESS_COOKIE, access, settings.ACCESS_TOKEN_EXPIRE)
        self._set_cookie(
            response, REFRESH_COOKIE, refresh, settings.REFRESH_TOKEN_EXPIRE
        )
        return {"message": "Logged in"}

    def refresh(self, request: Request, response: Response):
        refresh = request.cookies.get(REFRESH_COOKIE)
        if not refresh:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token"
            )

        payload = self.token_service.decode_token(refresh)
        if payload.type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
            )

        if payload.jti not in self.valid_refresh:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh revoked"
            )

        # ابطال قبلی
        self.valid_refresh.pop(payload.jti, None)

        # ساخت جدید
        new_access = self.token_service.create_token(
            subject=payload.sub,
            ttl=settings.ACCESS_TOKEN_EXPIRE,
            token_type="access",
            token_version=payload.tv,
        )
        new_jti = str(uuid.uuid4())
        new_refresh = self.token_service.create_token(
            subject=payload.sub,
            ttl=settings.REFRESH_TOKEN_EXPIRE,
            token_type="refresh",
            token_version=payload.tv,
            jti=new_jti,
        )
        self.valid_refresh[new_jti] = {"sub": payload.sub}

        self._set_cookie(
            response, ACCESS_COOKIE, new_access, settings.ACCESS_TOKEN_EXPIRE
        )
        self._set_cookie(
            response, REFRESH_COOKIE, new_refresh, settings.REFRESH_TOKEN_EXPIRE
        )
        return {"message": "Session renewed"}

    def logout(self, request: Request, response: Response):
        refresh = request.cookies.get(REFRESH_COOKIE)
        if refresh:
            try:
                payload = self.token_service.decode_token(refresh)
                self.valid_refresh.pop(payload.jti, None)
            except Exception:
                pass

        self._clear_cookie(response, ACCESS_COOKIE)
        self._clear_cookie(response, REFRESH_COOKIE)
        return {"message": "Logged out"}

    # ---------------- helper methods ----------------
    def _set_cookie(self, response: Response, name: str, value: str, ttl: timedelta):
        response.set_cookie(
            key=name,
            value=value,
            max_age=int(ttl.total_seconds()),
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            domain=settings.COOKIE_DOMAIN,
            path="/",
        )

    def _clear_cookie(self, response: Response, name: str):
        response.delete_cookie(
            key=name,
            domain=settings.COOKIE_DOMAIN,
            path="/",
            samesite=settings.COOKIE_SAMESITE,
        )
