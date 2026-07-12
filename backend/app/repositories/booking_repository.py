from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from typing import List, Optional
from uuid import UUID
from app.models.booking import ResourceBooking

class BookingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, booking: ResourceBooking) -> ResourceBooking:
        self.session.add(booking)
        await self.session.commit()
        await self.session.refresh(booking)
        return booking

    async def get_by_id(self, booking_id: UUID) -> Optional[ResourceBooking]:
        result = await self.session.execute(
            select(ResourceBooking).where(ResourceBooking.id == booking_id)
        )
        return result.scalars().first()

    async def get_all(self) -> List[ResourceBooking]:
        result = await self.session.execute(select(ResourceBooking))
        return list(result.scalars().all())

    async def check_overlap(self, asset_id: UUID, new_start, new_end) -> bool:
        stmt = select(ResourceBooking).where(
            and_(
                ResourceBooking.asset_id == asset_id,
                ResourceBooking.status.in_(["upcoming", "ongoing"]),
                ResourceBooking.start_time < new_end,
                ResourceBooking.end_time > new_start
            )
        )
        result = await self.session.execute(stmt)
        overlap = result.scalars().first()
        return overlap is not None

    async def update_status(self, booking: ResourceBooking, new_status: str) -> ResourceBooking:
        booking.status = new_status
        await self.session.commit()
        await self.session.refresh(booking)
        return booking
