import uuid
from typing import TypeVar, Generic, Type, Optional, List, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.base import Base

T = TypeVar('T', bound=Base)

class BaseRepository(Generic[T]):
    def __init__(self, model_class: Type[T], session: AsyncSession):
        self.model_class = model_class
        self.session = session

    async def get_by_id(self, id: uuid.UUID) -> Optional[T]:
        result = await self.session.execute(select(self.model_class).where(self.model_class.id == id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[T]:
        result = await self.session.execute(select(self.model_class).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, obj_in: dict) -> T:
        db_obj = self.model_class(**obj_in)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: T, obj_in: dict) -> T:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: T) -> None:
        await self.session.delete(db_obj)
        await self.session.commit()
