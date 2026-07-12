from fastapi import Request
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import SignupRequest, LoginRequest, ForgotPasswordRequest, ResetPasswordRequest, UserProfile
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.utils.security import decode_token
from app.utils.exceptions import UnauthorizedException
from app.config import settings

class AuthController:
    @staticmethod
    async def signup(data: SignupRequest, db: AsyncSession):
        service = AuthService(UserRepository(db))
        user = await service.signup(data)
        user_data = UserProfile.model_validate(user).model_dump(mode='json')
        return {"message": "Account created successfully", "user": user_data}

    @staticmethod
    async def login(data: LoginRequest, db: AsyncSession):
        service = AuthService(UserRepository(db))
        user, access_token, refresh_token, expires_in = await service.login(data)
        user_data = UserProfile.model_validate(user).model_dump(mode='json')
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": expires_in,
            "user": user_data
        }

    @staticmethod
    async def logout(request: Request):
        # We would ideally add the token to a blocklist here. For now, it's a no-op on backend.
        return {"message": "Logged out successfully"}

    @staticmethod
    async def forgot_password(data: ForgotPasswordRequest, db: AsyncSession):
        service = AuthService(UserRepository(db))
        token = await service.forgot_password(data.email)
        return {"message": "Password reset token generated", "reset_token": token}

    @staticmethod
    async def reset_password(data: ResetPasswordRequest, db: AsyncSession):
        payload = decode_token(data.token)
        if not payload or payload.get("role") != "reset":
            raise UnauthorizedException("Invalid or expired reset token")
        
        service = AuthService(UserRepository(db))
        await service.reset_password(payload.get("sub"), data.new_password)
        return {"message": "Password reset successfully"}

    @staticmethod
    async def me(current_user):
        return current_user
