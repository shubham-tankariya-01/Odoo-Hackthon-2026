from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import SignupRequest, LoginRequest, ForgotPasswordRequest, ResetPasswordRequest, TokenResponse, UserProfile
from app.schemas.common import MessageResponse
from app.controllers.auth_controller import AuthController
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from typing import Any

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=Any,
             status_code=status.HTTP_201_CREATED)
async def signup(data: SignupRequest, db: AsyncSession = Depends(get_db)):
    return await AuthController.signup(data, db)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await AuthController.login(data, db)


@router.post("/logout", response_model=MessageResponse)
async def logout(request: Request,
                 current_user: User = Depends(get_current_user)):
    # We pass request to controller in a real app to invalidate token, simple
    # implementation for now
    return await AuthController.logout(request)


@router.post("/forgot-password", response_model=Any)
async def forgot_password(data: ForgotPasswordRequest,
                          db: AsyncSession = Depends(get_db)):
    return await AuthController.forgot_password(data, db)


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(data: ResetPasswordRequest,
                         db: AsyncSession = Depends(get_db)):
    return await AuthController.reset_password(data, db)


@router.get("/me", response_model=UserProfile)
async def me(current_user: User = Depends(get_current_user)):
    return await AuthController.me(current_user)
