from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class ResourceBooking(BaseModel):
    __tablename__ = "resource_bookings"

    asset_id = Column(UUID(as_uuid=True), nullable=False)
    booked_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default="upcoming", nullable=False)
