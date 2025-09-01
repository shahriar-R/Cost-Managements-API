from pydantic import BaseModel, Field, condecimal, constr


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


# input model
class Expense(BaseModel):

    description: constr(
        strip_whitespace=True,
        min_length=3,
        max_length=100,
        pattern=r"^[a-zA-Z0-9\s\-\.,]+$",
    ) = Field(..., description="توضیح هزینه")

    amount: condecimal(gt=0, max_digits=10, decimal_places=2) = Field(
        ..., description="مبلغ هزینه (مثبت)"
    )


# output model
class ExpenseOut(Expense):
    id: int = Field(..., gt=0, description="شناسه یکتا (مثبت)")
