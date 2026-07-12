from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserUpdate, UserRoleUpdate
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.repositories.department_repository import DepartmentRepository
from app.utils.responses import paginated_response
from app.schemas.auth import UserProfile


class UserController:
    @staticmethod
    async def get_all(db: AsyncSession, department_id: Optional[UUID] = None, role: Optional[str]
                      = None, status: Optional[str] = None, page: int = 1, page_size: int = 20):
        service = UserService(UserRepository(db), DepartmentRepository(db))
        skip = (page - 1) * page_size
        users, total = await service.get_all(department_id, role, status, skip, page_size)
        items = [
            UserProfile.model_validate(u).model_dump(
                mode='json') for u in users]
        return paginated_response(items, total, page, page_size)

    @staticmethod
    async def get_by_id(user_id: UUID, db: AsyncSession):
        service = UserService(UserRepository(db), DepartmentRepository(db))
        user = await service.get_by_id(user_id)
        return UserProfile.model_validate(user).model_dump(mode='json')

    @staticmethod
    async def update(user_id: UUID, data: UserUpdate, db: AsyncSession):
        service = UserService(UserRepository(db), DepartmentRepository(db))
        user = await service.update(user_id, data)
        return UserProfile.model_validate(user).model_dump(mode='json')

    @staticmethod
    async def promote(user_id: UUID, data: UserRoleUpdate,
                      db: AsyncSession, current_user_id: UUID):
        service = UserService(UserRepository(db), DepartmentRepository(db))
        user = await service.promote(user_id, data, current_user_id)
        return UserProfile.model_validate(user).model_dump(mode='json')
