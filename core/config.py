from datetime import timedelta


class Settings:
    SECRET_KEY: str = "CHANGE_ME"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE: timedelta = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRE: timedelta = timedelta(days=7)
    COOKIE_SECURE: bool = True
    COOKIE_SAMESITE: str = "lax"
    COOKIE_DOMAIN: str | None = None


settings = Settings()
