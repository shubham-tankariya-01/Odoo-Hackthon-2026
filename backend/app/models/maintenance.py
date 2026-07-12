from enum import Enum
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class MaintenancePriority(str, Enum):
    low      = "low"
    medium   = "medium"
    high     = "high"
    critical = "critical"


class MaintenanceStatus(str, Enum):
    pending     = "pending"
    approved    = "approved"
    rejected    = "rejected"
    assigned    = "assigned"
    in_progress = "in_progress"
    resolved    = "resolved"


class MaintenanceRequest(BaseModel):
    __tablename__ = "maintenance_requests"

    asset_id         = Column(UUID(as_uuid=True), ForeignKey("assets.id"),  nullable=False)
    raised_by_id     = Column(UUID(as_uuid=True), ForeignKey("users.id"),   nullable=False)
    description      = Column(Text, nullable=False)
    priority         = Column(String(20), default=MaintenancePriority.medium, nullable=False)
    status           = Column(String(20), default=MaintenanceStatus.pending,  nullable=False)
    approved_by_id   = Column(UUID(as_uuid=True), ForeignKey("users.id"),   nullable=True)
    technician_id    = Column(UUID(as_uuid=True), ForeignKey("users.id"),   nullable=True)
    resolution_notes = Column(Text, nullable=True)
    photo_url        = Column(String(500), nullable=True)
    resolved_at      = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    asset       = relationship("Asset", foreign_keys=[asset_id], back_populates="maintenance_requests")
    raised_by   = relationship("User", foreign_keys=[raised_by_id])
    approved_by = relationship("User", foreign_keys=[approved_by_id])
    technician  = relationship("User", foreign_keys=[technician_id])
