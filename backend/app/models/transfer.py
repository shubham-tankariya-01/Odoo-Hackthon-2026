from enum import Enum
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class TransferStatus(str, Enum):
    requested = "requested"
    approved = "approved"
    rejected = "rejected"
    completed = "completed"
    cancelled = "cancelled"


class Transfer(BaseModel):
    __tablename__ = "transfers"

    asset_id = Column(
        UUID(
            as_uuid=True),
        ForeignKey("assets.id"),
        nullable=False)
    from_employee_id = Column(
        UUID(
            as_uuid=True),
        ForeignKey("users.id"),
        nullable=False)
    to_employee_id = Column(
        UUID(
            as_uuid=True),
        ForeignKey("users.id"),
        nullable=False)
    status = Column(
        String(20),
        default=TransferStatus.requested,
        nullable=False)
    requested_by_id = Column(
        UUID(
            as_uuid=True),
        ForeignKey("users.id"),
        nullable=False)
    approved_by_id = Column(
        UUID(
            as_uuid=True),
        ForeignKey("users.id"),
        nullable=True)
    reason = Column(Text, nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    asset = relationship("Asset", foreign_keys=[asset_id])
    from_employee = relationship("User", foreign_keys=[from_employee_id])
    to_employee = relationship("User", foreign_keys=[to_employee_id])
    requested_by = relationship("User", foreign_keys=[requested_by_id])
    approved_by = relationship("User", foreign_keys=[approved_by_id])
