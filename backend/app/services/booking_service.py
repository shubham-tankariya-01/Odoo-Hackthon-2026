from uuid import UUID
from app.models.booking import ResourceBooking
from app.schemas.booking import BookingCreate
from app.repositories.booking_repository import BookingRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

class BookingOverlapError(Exception):
    pass

class BookingService:
    def __init__(self, session: AsyncSession):
        self.repo = BookingRepository(session)

    async def create_booking(self, booking_in: BookingCreate, user_id: UUID) -> ResourceBooking:
        if booking_in.start_time >= booking_in.end_time:
            raise ValueError("End time must be after start time")
            
        is_overlapping = await self.repo.check_overlap(
            booking_in.asset_id, 
            booking_in.start_time, 
            booking_in.end_time
        )
        if is_overlapping:
            raise BookingOverlapError("Time slot is already booked for this asset.")

        new_booking = ResourceBooking(
            asset_id=booking_in.asset_id,
            booked_by=user_id,
            start_time=booking_in.start_time,
            end_time=booking_in.end_time,
            status="upcoming"
        )
        return await self.repo.create(new_booking)

    async def list_bookings(self) -> List[ResourceBooking]:
        return await self.repo.get_all()

    async def cancel_booking(self, booking_id: UUID, user_id: UUID) -> ResourceBooking:
        booking = await self.repo.get_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        if booking.booked_by != user_id:
            raise PermissionError("Cannot cancel another user's booking")
        
        return await self.repo.update_status(booking, "cancelled")

    async def get_booking(self, booking_id: UUID) -> ResourceBooking:
        booking = await self.repo.get_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        return booking

    async def reschedule_booking(self, booking_id: UUID, user_id: UUID, new_start, new_end) -> ResourceBooking:
        booking = await self.repo.get_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        if booking.booked_by != user_id:
            raise PermissionError("Cannot modify another user's booking")
        if new_start >= new_end:
            raise ValueError("End time must be after start time")

        conflicts = await self.repo.get_conflicting_bookings(booking.asset_id, new_start, new_end, exclude_booking_id=booking_id)
        if conflicts:
            raise BookingOverlapError("Time slot overlaps with an existing booking")

        booking.start_time = new_start
        booking.end_time = new_end
        
        await self.repo.session.commit()
        await self.repo.session.refresh(booking)
        return booking

    async def check_availability(self, asset_id: UUID, start_time, end_time):
        conflicts = await self.repo.get_conflicting_bookings(asset_id, start_time, end_time)
        return {
            "asset_id": asset_id,
            "start_time": start_time,
            "end_time": end_time,
            "is_available": len(conflicts) == 0,
            "conflicts": [{"id": c.id, "start_time": c.start_time, "end_time": c.end_time} for c in conflicts]
        }

    async def get_calendar(self, asset_id: UUID, year: int, month: int):
        bookings = await self.repo.get_by_asset_and_month(asset_id, year, month)
        items = []
        for b in bookings:
            items.append({
                "id": b.id,
                "date": b.start_time.strftime("%Y-%m-%d"),
                "start_time": b.start_time.strftime("%H:%M"),
                "end_time": b.end_time.strftime("%H:%M"),
                "status": b.status
            })
        return {
            "asset_id": asset_id,
            "month": f"{year}-{month:02d}",
            "bookings": items
        }
