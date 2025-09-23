from fastapi import APIRouter, Response, Request
from schemas import LoginInput
from auth.services import AuthService
from auth.repositories import UserRepository
from auth.security import PasswordHasher
from auth.tokens import TokenService

router = APIRouter(prefix="/auth", tags=["auth"])

# (Dependency Injection)
password_hasher = PasswordHasher()
user_repo = UserRepository(password_hasher)
token_service = TokenService()
auth_service = AuthService(user_repo, token_service)


@router.post("/login")
def login(data: LoginInput, response: Response):
    return auth_service.login(data.username, data.password, response)


@router.post("/refresh")
def refresh(request: Request, response: Response):
    return auth_service.refresh(request, response)


@router.post("/logout")
def logout(request: Request, response: Response):
    return auth_service.logout(request, response)
