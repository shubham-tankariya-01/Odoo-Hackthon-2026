from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.schemas.booking import (
    BookingCreate, BookingResponse, BookingUpdate,
    CalendarResponse, AvailabilityResponse
)
from app.controllers.booking_controller import BookingController
from app.dependencies.database import get_db

# Assuming Member 1 has built get_current_user in dependencies.auth
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingResponse)
async def create_booking_route(booking_in: BookingCreate, current_user=Depends(
        get_current_user), db: AsyncSession = Depends(get_db)):
    return await BookingController.create_booking(booking_in, current_user.id, db)


@router.get("/", response_model=List[BookingResponse])
async def list_bookings_route(db: AsyncSession = Depends(get_db)):
    return await BookingController.get_bookings(db)


@router.get("/calendar", response_model=CalendarResponse)
async def get_booking_calendar(
        asset_id: UUID, month: str, db: AsyncSession = Depends(get_db)):
    return await BookingController.get_calendar(asset_id, month, db)


@router.get("/availability", response_model=AvailabilityResponse)
async def check_booking_availability(
        asset_id: UUID, start: str, end: str, db: AsyncSession = Depends(get_db)):
    return await BookingController.check_availability(asset_id, start, end, db)


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_single_booking_route(
        booking_id: UUID, db: AsyncSession = Depends(get_db)):
    return await BookingController.get_booking(booking_id, db)


@router.patch("/{booking_id}", response_model=BookingResponse)
async def reschedule_booking_route(booking_id: UUID, booking_update: BookingUpdate, current_user=Depends(
        get_current_user), db: AsyncSession = Depends(get_db)):
    return await BookingController.reschedule_booking(booking_id, current_user.id, booking_update, db)


@router.delete("/{booking_id}", response_model=BookingResponse)
async def cancel_booking_route(booking_id: UUID, current_user=Depends(
        get_current_user), db: AsyncSession = Depends(get_db)):
    return await BookingController.cancel_booking(booking_id, current_user.id, db)
