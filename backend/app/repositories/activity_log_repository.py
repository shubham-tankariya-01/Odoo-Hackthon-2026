from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from uuid import UUID
from app.models.activity_log import ActivityLog

class ActivityLogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, log: ActivityLog) -> ActivityLog:
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log

    async def get_all(self) -> List[ActivityLog]:
        result = await self.session.execute(
            select(ActivityLog).order_by(ActivityLog.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_recipient(self, recipient_id: UUID) -> List[ActivityLog]:
        result = await self.session.execute(
            select(ActivityLog)
            .where(ActivityLog.recipient_user_id == recipient_id)
            .order_by(ActivityLog.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, log_id: UUID) -> Optional[ActivityLog]:
        result = await self.session.execute(
            select(ActivityLog).where(ActivityLog.id == log_id)
        )
        return result.scalars().first()

    async def mark_as_read(self, log: ActivityLog) -> ActivityLog:
        log.is_read = True
        await self.session.commit()
        await self.session.refresh(log)
        return log
