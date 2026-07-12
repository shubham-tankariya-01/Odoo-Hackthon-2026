import uuid
from typing import Optional, Sequence, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.maintenance import MaintenanceRequest, MaintenanceStatus
from app.repositories.base_repository import BaseRepository


class MaintenanceRepository(BaseRepository[MaintenanceRequest]):
    def __init__(self, session: AsyncSession):
        super().__init__(MaintenanceRequest, session)

    async def search(
        self,
        asset_id: Optional[uuid.UUID] = None,
        raised_by_id: Optional[uuid.UUID] = None,
        technician_id: Optional[uuid.UUID] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[Sequence[MaintenanceRequest], int]:
        query = select(MaintenanceRequest)

        if asset_id:
            query = query.where(MaintenanceRequest.asset_id == asset_id)
        if raised_by_id:
            query = query.where(MaintenanceRequest.raised_by_id == raised_by_id)
        if technician_id:
            query = query.where(MaintenanceRequest.technician_id == technician_id)
        if status:
            query = query.where(MaintenanceRequest.status == status)
        if priority:
            query = query.where(MaintenanceRequest.priority == priority)

        count_result = await self.session.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = count_result.scalar() or 0

        query = query.order_by(MaintenanceRequest.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all(), total
