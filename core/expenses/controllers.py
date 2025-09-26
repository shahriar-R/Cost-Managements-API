from fastapi import APIRouter, Depends, HTTPException, status
from core.db.schemas import Expense, ExpenseOut
from dependencies import get_current_user

router = APIRouter(prefix="/expenses", tags=["expenses"])


expenses: dict[int, ExpenseOut] = {}
next_id = 1


@router.post("/", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(expense: Expense, username: str = Depends(get_current_user)):
    global next_id
    new_expense = ExpenseOut(id=next_id, **expense.dict())
    expenses[next_id] = new_expense
    next_id += 1
    return new_expense


@router.get("/", response_model=list[ExpenseOut])
def get_all_expenses(username: str = Depends(get_current_user)):
    return list(expenses.values())


@router.get("/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int, username: str = Depends(get_current_user)):
    if expense_id not in expenses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )
    return expenses[expense_id]


@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(
    expense_id: int, expense: Expense, username: str = Depends(get_current_user)
):
    if expense_id not in expenses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )
    updated_expense = ExpenseOut(id=expense_id, **expense.dict())
    expenses[expense_id] = updated_expense
    return updated_expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, username: str = Depends(get_current_user)):
    if expense_id not in expenses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )
    del expenses[expense_id]
    return
