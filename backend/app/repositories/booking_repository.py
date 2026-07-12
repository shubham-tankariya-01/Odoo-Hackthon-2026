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

    async def get_conflicting_bookings(self, asset_id: UUID, new_start, new_end, exclude_booking_id: Optional[UUID] = None) -> List[ResourceBooking]:
        stmt = select(ResourceBooking).where(
            and_(
                ResourceBooking.asset_id == asset_id,
                ResourceBooking.status.in_(["upcoming", "ongoing"]),
                ResourceBooking.start_time < new_end,
                ResourceBooking.end_time > new_start
            )
        )
        if exclude_booking_id:
            stmt = stmt.where(ResourceBooking.id != exclude_booking_id)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_asset_and_month(self, asset_id: UUID, year: int, month: int) -> List[ResourceBooking]:
        from datetime import datetime, timezone
        import calendar
        _, last_day = calendar.monthrange(year, month)
        
        start_date = datetime(year, month, 1, tzinfo=timezone.utc)
        end_date = datetime(year, month, last_day, 23, 59, 59, tzinfo=timezone.utc)

        stmt = select(ResourceBooking).where(
            and_(
                ResourceBooking.asset_id == asset_id,
                ResourceBooking.start_time >= start_date,
                ResourceBooking.start_time <= end_date,
                ResourceBooking.status != "cancelled"
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
