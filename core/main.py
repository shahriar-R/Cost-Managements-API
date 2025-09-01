import uvicorn
from fastapi import FastAPI

from expenses.controllers import router as expenses_router
from auth.controllers import router as auth_router


from schemas import Expense, ExpenseOut

app = FastAPI()
app.include_router(auth_router)
app.include_router(expenses_router)
