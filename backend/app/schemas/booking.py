from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional


class BookingCreate(BaseModel):
    asset_id: UUID
    start_time: datetime
    end_time: datetime


class BookingUpdate(BaseModel):
    start_time: datetime
    end_time: datetime


class BookingResponse(BaseModel):
    id: UUID
    asset_id: UUID
    booked_by: UUID
    start_time: datetime
    end_time: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)


class AvailabilityResponse(BaseModel):
    asset_id: UUID
    start_time: datetime
    end_time: datetime
    is_available: bool
    conflicts: list = []


class CalendarBookingItem(BaseModel):
    id: UUID
    date: str
    start_time: str
    end_time: str
    status: str


class CalendarResponse(BaseModel):
    asset_id: UUID
    month: str
    bookings: list[CalendarBookingItem]
