from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.schemas.booking import BookingCreate, BookingResponse
from app.controllers.booking_controller import BookingController
from app.dependencies.database import get_db

# Assuming Member 1 has built get_current_user in dependencies.auth
try:
    from app.dependencies.auth import get_current_user
except ImportError:
    # Fallback if not yet implemented by Member 1
    def get_current_user():
        class MockUser:
            id = UUID("11111111-1111-1111-1111-111111111111")
        return MockUser()

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse)
async def create_booking_route(booking_in: BookingCreate, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await BookingController.create_booking(booking_in, current_user.id, db)

@router.get("/", response_model=List[BookingResponse])
async def list_bookings_route(db: AsyncSession = Depends(get_db)):
    return await BookingController.get_bookings(db)

@router.delete("/{booking_id}", response_model=BookingResponse)
async def cancel_booking_route(booking_id: UUID, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await BookingController.cancel_booking(booking_id, current_user.id, db)
