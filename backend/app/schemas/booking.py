from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional

class BookingCreate(BaseModel):
    asset_id: UUID
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
