from fastapi import FastAPI, HTTPException, status, Request

app = FastAPI()


expenses = {}
current_id = 0


# create cost
@app.post("/expenses", status_code=status.HTTP_201_CREATED)
async def create_expense(request: Request):
    global current_id
    data = await request.json()

    if "description" not in data or "amount" not in data:
        raise HTTPException(
            status_code=400, detail="Fields 'description' and 'amount' are required"
        )

    current_id += 1
    expense = {
        "id": current_id,
        "description": str(data["description"]),
        "amount": float(data["amount"]),
    }
    expenses[current_id] = expense
    return expense


# GET Costs
@app.get("/expenses")
def get_expenses():
    return list(expenses.values())


# get cost by ID
@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    expense = expenses.get(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


# update cost by ID
@app.put("/expenses/{expense_id}")
async def update_expense(expense_id: int, request: Request):
    data = await request.json()
    expense = expenses.get(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if "description" in data:
        expense["description"] = str(data["description"])
    if "amount" in data:
        expense["amount"] = float(data["amount"])

    expenses[expense_id] = expense
    return expense


# delete cost by ID
@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    del expenses[expense_id]
    return None
