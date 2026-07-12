from fastapi import HTTPException
from app.schemas.auth import SignupRequest, LoginRequest
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.utils.constants import UserRole
from app.utils.exceptions import ConflictException, UnauthorizedException, NotFoundException
from app.config import settings


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def signup(self, data: SignupRequest) -> User:
        if await self.user_repo.email_exists(data.email):
            raise ConflictException("Email already registered")

        user_in = {
            "name": data.name,
            "email": data.email,
            "hashed_password": hash_password(data.password),
            "role": data.role if hasattr(data, 'role') and data.role else UserRole.EMPLOYEE
        }
        return await self.user_repo.create(user_in)

    async def login(self, data: LoginRequest) -> tuple[User, str, str, int]:
        user = await self.user_repo.get_by_email(data.email)
        if not user or not verify_password(
                data.password, user.hashed_password):  # type: ignore
            raise UnauthorizedException("Invalid email or password")

        if user.status != "active":
            raise UnauthorizedException("Account is deactivated")

        access_token = create_access_token(
            subject=user.id, role=user.role)  # type: ignore
        refresh_token = create_refresh_token(
            subject=user.id, role=user.role)  # type: ignore
        expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

        return user, access_token, refresh_token, expires_in

    async def get_me(self, user_id: str) -> User:
        user = await self.user_repo.get_by_id(user_id)  # type: ignore
        if not user:
            raise NotFoundException("User not found")
        return user

    async def forgot_password(self, email: str) -> str:
        user = await self.user_repo.get_by_email(email)
        if not user:
            # Don't reveal if email exists, just return a fake token or success anyway in a real app.
            # But for hackathon, let's return a valid one for simplicity if
            # they exist.
            raise NotFoundException("User not found")

        # In a real app we'd save this to DB and send an email
        reset_token = create_access_token(
            subject=user.id,
            role="reset",
            expires_delta=None)  # short lived
        return reset_token

    async def reset_password(self, user_id: str, new_password: str) -> None:
        user = await self.user_repo.get_by_id(user_id)  # type: ignore
        if not user:
            raise NotFoundException("User not found")

        await self.user_repo.update(user, {"hashed_password": hash_password(new_password)})
