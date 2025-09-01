from fastapi import FastAPI, HTTPException
from typing import Dict
from decimal import Decimal

from models import Expense, ExpenseOut


app = FastAPI()

expenses: Dict[int, ExpenseOut] = {}
next_id = 1


@app.post("/expenses", response_model=ExpenseOut, status_code=201)
def create_expense(expense: Expense):
    global next_id
    new_expense = ExpenseOut(id=next_id, **expense.dict())
    expenses[next_id] = new_expense
    next_id += 1
    return new_expense


@app.get("/expenses", response_model=list[ExpenseOut])
def get_all_expenses():
    return list(expenses.values())


@app.get("/expenses/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expenses[expense_id]


@app.put("/expenses/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, expense: Expense):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    updated_expense = ExpenseOut(id=expense_id, **expense.dict())
    expenses[expense_id] = updated_expense
    return updated_expense


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    del expenses[expense_id]
    return
