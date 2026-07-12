import uuid
from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.department import Department
from app.models.user import User
from app.repositories.base_repository import BaseRepository

class DepartmentRepository(BaseRepository[Department]):
    def __init__(self, session: AsyncSession):
        super().__init__(Department, session)

    async def get_by_name(self, name: str) -> Optional[Department]:
        result = await self.session.execute(select(Department).where(Department.name == name))
        return result.scalars().first()

    async def get_children(self, parent_id: uuid.UUID) -> Sequence[Department]:
        result = await self.session.execute(select(Department).where(Department.parent_department_id == parent_id))
        return result.scalars().all()

    async def get_member_count(self, department_id: uuid.UUID) -> int:
        result = await self.session.execute(
            select(func.count(User.id)).where(User.department_id == department_id, User.status == "active")
        )
        return result.scalar() or 0
