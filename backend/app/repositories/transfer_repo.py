import uuid
from typing import Optional, Sequence, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.models.transfer import Transfer
from app.repositories.base_repository import BaseRepository


class TransferRepository(BaseRepository[Transfer]):
    def __init__(self, session: AsyncSession):
        super().__init__(Transfer, session)

    async def search(
        self,
        asset_id: Optional[uuid.UUID] = None,
        from_employee_id: Optional[uuid.UUID] = None,
        to_employee_id: Optional[uuid.UUID] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[Sequence[Transfer], int]:
        query = select(Transfer)

        if asset_id:
            query = query.where(Transfer.asset_id == asset_id)
        if from_employee_id:
            query = query.where(Transfer.from_employee_id == from_employee_id)
        if to_employee_id:
            query = query.where(Transfer.to_employee_id == to_employee_id)
        if status:
            query = query.where(Transfer.status == status)

        count_result = await self.session.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = count_result.scalar() or 0

        query = query.order_by(Transfer.created_at.desc()
                               ).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all(), total
