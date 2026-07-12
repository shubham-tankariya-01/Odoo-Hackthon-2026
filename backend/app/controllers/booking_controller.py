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

    @staticmethod
    async def get_booking(booking_id: UUID, db: AsyncSession):
        service = BookingService(db)
        try:
            return await service.get_booking(booking_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    async def reschedule_booking(booking_id: UUID, user_id: UUID, booking_update, db: AsyncSession):
        service = BookingService(db)
        try:
            return await service.reschedule_booking(booking_id, user_id, booking_update.start_time, booking_update.end_time)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except BookingOverlapError as e:
            raise HTTPException(status_code=409, detail=str(e))

    @staticmethod
    async def get_calendar(asset_id: UUID, month: str, db: AsyncSession):
        service = BookingService(db)
        try:
            year_int, month_int = map(int, month.split('-'))
            return await service.get_calendar(asset_id, year_int, month_int)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid month format, expected YYYY-MM")

    @staticmethod
    async def check_availability(asset_id: UUID, start: str, end: str, db: AsyncSession):
        from datetime import datetime
        service = BookingService(db)
        try:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
            return await service.check_availability(asset_id, start_dt, end_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format")
