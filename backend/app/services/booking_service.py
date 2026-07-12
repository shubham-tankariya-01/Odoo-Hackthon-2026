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
