from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class ResourceBooking(BaseModel):
    __tablename__ = "resource_bookings"

    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default="pending", nullable=False)
