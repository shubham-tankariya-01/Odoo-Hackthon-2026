from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.schemas.booking import BookingCreate
from app.services.booking_service import BookingService, BookingOverlapError

class BookingController:
    @staticmethod
    async def create_booking(booking_in: BookingCreate, user_id: UUID, db: AsyncSession):
        service = BookingService(db)
        try:
            return await service.create_booking(booking_in, user_id)
        except BookingOverlapError as e:
            raise HTTPException(status_code=409, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_bookings(db: AsyncSession):
        service = BookingService(db)
        return await service.list_bookings()

    @staticmethod
    async def cancel_booking(booking_id: UUID, user_id: UUID, db: AsyncSession):
        service = BookingService(db)
        try:
            return await service.cancel_booking(booking_id, user_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))
