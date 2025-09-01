import uuid
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.config import settings
from app.schemas import TokenPayload


class TokenService:
    def __init__(
        self, secret: str = settings.SECRET_KEY, algorithm: str = settings.ALGORITHM
    ):
        self.secret = secret
        self.algorithm = algorithm

    def _now(self):
        return datetime.now(timezone.utc)

    def create_token(
        self,
        subject: str,
        ttl: timedelta,
        token_type: str,
        token_version: int,
        jti: str | None = None,
    ) -> str:
        jti = jti or str(uuid.uuid4())
        now = self._now()
        payload = {
            "sub": subject,
            "type": token_type,
            "jti": jti,
            "iat": int(now.timestamp()),
            "exp": int((now + ttl).timestamp()),
            "tv": token_version,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return TokenPayload(**payload)
        except JWTError as e:
            raise ValueError("Invalid or expired token") from e
