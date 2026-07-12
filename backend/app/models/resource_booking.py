from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class ResourceBooking(BaseModel):
    __tablename__ = "resource_bookings"
    
    asset_id = Column(UUID(as_uuid=True), ForeignKey('assets.id'), nullable=False)
    booked_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), nullable=False)
    
    asset = relationship("Asset")
    user = relationship("User")
