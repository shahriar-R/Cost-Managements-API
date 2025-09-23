import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from expenses.controllers import router as expenses_router
from auth.controllers import router as auth_router
from exceptions import CostNotFoundException

app = FastAPI()
app.include_router(auth_router)
app.include_router(expenses_router)


@app.exception_handler(CostNotFoundException)
async def cost_not_found_exception_handler(
    request: Request, exc: CostNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={"status": "error", "message": exc.message},
    )


fake_db = {1: {"id": 1, "title": "ناهار", "amount": 120000}}


@app.get("/costs/{cost_id}")
async def get_cost(cost_id: int):
    if cost_id not in fake_db:
        raise CostNotFoundException(cost_id)  
    return fake_db[cost_id]
