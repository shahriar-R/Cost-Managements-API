import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from expenses.controllers import router as expenses_router
from auth.controllers import router as auth_router
from exceptions import CostNotFoundException
from databases import database
from auth.repositories import UserRepository
from auth.security import PasswordHasher

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


@app.get("/costs/{cost_id}")
async def get_cost(cost_id: int):
    if cost_id not in fake_db:
        raise CostNotFoundException(cost_id)  # 🔹 اینجاست که خطا رو صدا می‌زنیم
    return fake_db[cost_id]


@app.on_event("startup")
async def startup():
    await database.connect()
    # create a test user if not exists
    password_hasher = PasswordHasher()
    user_repo = UserRepository(password_hasher)
    if not await user_repo.get_by_username("testuser"):
        await user_repo.create_user(username="testuser", password="testpassword")


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
