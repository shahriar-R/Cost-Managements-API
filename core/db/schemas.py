from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LoginInput(BaseModel):
    username: str
    password: str


class MeOut(BaseModel):
    username: str


class TokenPayload(BaseModel):
    sub: str
    type: str
    jti: str
    tv: int
    exp: int


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


# ---------- Expense Schemas ----------
class ExpenseBase(BaseModel):
    title: str
    amount: float


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseOut(ExpenseBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True
