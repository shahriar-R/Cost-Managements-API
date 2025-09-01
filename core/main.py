import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Dict

from models import Expense, ExpenseOut
from auth import (
    create_access_token,
    create_refresh_token,
    verify_token,
    get_current_user,
)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

expenses: Dict[int, ExpenseOut] = {}
next_id = 1


@app.post("/expenses", response_model=ExpenseOut, status_code=201)
def create_expense(expense: Expense, username: str = Depends(get_current_user)):
    global next_id
    new_expense = ExpenseOut(id=next_id, **expense.dict())
    expenses[next_id] = new_expense
    next_id += 1
    return new_expense


@app.get("/expenses", response_model=list[ExpenseOut])
def get_all_expenses(username: str = Depends(get_current_user)):
    return list(expenses.values())


@app.get("/expenses/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int, username: str = Depends(get_current_user)):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expenses[expense_id]


@app.put("/expenses/{expense_id}", response_model=ExpenseOut)
def update_expense(
    expense_id: int, expense: Expense, username: str = Depends(get_current_user)
):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    updated_expense = ExpenseOut(id=expense_id, **expense.model_dump())
    expenses[expense_id] = updated_expense
    return updated_expense


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int, username: str = Depends(get_current_user)):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    del expenses[expense_id]
    return


@app.post("/login")
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(oauth2_scheme),
):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user["username"])
    refresh_token = create_refresh_token(user["username"])

    # ذخیره در کوکی‌های امن
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Strict",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
    )

    return {"message": "Login successful"}


@app.post("/refresh")
def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    username = verify_token(refresh_token)
    if username not in fake_users_db:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token(username)
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=True,
        samesite="Strict",
    )
    return {"message": "Access token refreshed"}


@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
