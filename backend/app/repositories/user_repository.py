import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def email_exists(self, email: str) -> bool:
        user = await self.get_by_email(email)
        return user is not None
        
    async def get_all_with_filters(self, department_id: Optional[uuid.UUID] = None, role: Optional[str] = None, status: Optional[str] = None, skip: int = 0, limit: int = 100):
        query = select(User)
        if department_id:
            query = query.where(User.department_id == department_id)
        if role:
            query = query.where(User.role == role)
        if status:
            query = query.where(User.status == status)
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
