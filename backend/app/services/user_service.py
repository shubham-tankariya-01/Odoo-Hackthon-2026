from typing import List, Tuple, Optional
from uuid import UUID
from app.schemas.user import UserUpdate, UserRoleUpdate
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.department_repository import DepartmentRepository
from app.utils.exceptions import NotFoundException, ValidationException
from app.utils.constants import UserRole


class UserService:
    def __init__(self, user_repo: UserRepository,
                 dept_repo: DepartmentRepository):
        self.user_repo = user_repo
        self.dept_repo = dept_repo

    async def get_all(self, department_id: Optional[UUID] = None, role: Optional[str] = None,
                      status: Optional[str] = None, skip: int = 0, limit: int = 100) -> Tuple[List[User], int]:
        users = await self.user_repo.get_all_with_filters(department_id, role, status, skip, limit)
        return users, len(users)

    async def get_by_id(self, user_id: UUID) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return user

    async def update(self, user_id: UUID, data: UserUpdate) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")

        if data.department_id:
            dept = await self.dept_repo.get_by_id(data.department_id)
            if not dept or dept.status != "active":
                raise ValidationException("Invalid or inactive department")

        # We don't handle deactivation rules here yet, assuming basic update
        user_in = data.model_dump(exclude_unset=True)
        return await self.user_repo.update(user, user_in)

    async def promote(self, user_id: UUID, data: UserRoleUpdate,
                      promoter_id: UUID) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")

        if user.status != "active":
            raise ValidationException("Cannot promote an inactive user")

        promoter = await self.user_repo.get_by_id(promoter_id)

        # Admins can promote anyone to anything.
        if promoter.role != UserRole.ADMIN:  # type: ignore
            raise ValidationException("Only admins can promote users")

        return await self.user_repo.update(user, {"role": data.role, "promoted_by": promoter_id})
