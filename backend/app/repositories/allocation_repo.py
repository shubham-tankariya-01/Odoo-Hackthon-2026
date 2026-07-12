import uuid
from datetime import date
from typing import Optional, Sequence, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.models.allocation import Allocation
from app.repositories.base_repository import BaseRepository


class AllocationRepository(BaseRepository[Allocation]):
    def __init__(self, session: AsyncSession):
        super().__init__(Allocation, session)

    async def get_active_by_asset(
            self, asset_id: uuid.UUID) -> Optional[Allocation]:
        """Returns the single active allocation for an asset, or None."""
        result = await self.session.execute(
            select(Allocation).where(
                and_(
                    Allocation.asset_id == asset_id,
                    Allocation.is_active == True)
            )
        )
        return result.scalars().first()

    async def get_by_employee(
        self, employee_id: uuid.UUID, active_only: bool = False, skip: int = 0, limit: int = 20
    ) -> Tuple[Sequence[Allocation], int]:
        query = select(Allocation).where(Allocation.employee_id == employee_id)
        if active_only:
            query = query.where(Allocation.is_active == True)

        count_result = await self.session.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar() or 0

        query = query.order_by(
            Allocation.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all(), total

    async def search(
        self,
        employee_id: Optional[uuid.UUID] = None,
        department_id: Optional[uuid.UUID] = None,
        asset_id: Optional[uuid.UUID] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[Sequence[Allocation], int]:
        query = select(Allocation)

        if employee_id:
            query = query.where(Allocation.employee_id == employee_id)
        if department_id:
            query = query.where(Allocation.department_id == department_id)
        if asset_id:
            query = query.where(Allocation.asset_id == asset_id)
        if is_active is not None:
            query = query.where(Allocation.is_active == is_active)

        count_result = await self.session.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar() or 0

        query = query.order_by(
            Allocation.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all(), total

    async def get_overdue(self, today: date) -> Sequence[Allocation]:
        """Return all active allocations where expected_return_date < today."""
        result = await self.session.execute(
            select(Allocation).where(
                and_(
                    Allocation.is_active == True,
                    Allocation.expected_return_date.isnot(None),
                    Allocation.expected_return_date < today,
                )
            ).order_by(Allocation.expected_return_date)
        )
        return result.scalars().all()
