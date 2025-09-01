from typing import Dict, Optional
from app.auth.models import User
from app.auth.security import PasswordHasher


class UserRepository:
    """
    فقط مسئول دسترسی به دیتابیس کاربران است.
    در اینجا DB فیک داریم.
    """

    def __init__(self, password_hasher: PasswordHasher):
        self.password_hasher = password_hasher
        self._users: Dict[str, User] = {
            "alice": User(
                username="alice",
                password_hash=password_hasher.hash("password123"),
                token_version=1,
            )
        }

    def get_by_username(self, username: str) -> Optional[User]:
        return self._users.get(username)

    def verify_user(self, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(username)
        if user and self.password_hasher.verify(password, user.password_hash):
            return user
        return None
