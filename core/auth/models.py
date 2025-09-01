from dataclasses import dataclass


@dataclass
class User:
    username: str
    password_hash: str
    token_version: int = 1
