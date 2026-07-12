from enum import Enum
from sqlalchemy import Column, String, Boolean, Date, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class AllocationStatus(str, Enum):
    active   = "active"
    returned = "returned"
    cancelled = "cancelled"


class Allocation(BaseModel):
    __tablename__ = "asset_allocations"

    asset_id             = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    employee_id          = Column(UUID(as_uuid=True), ForeignKey("users.id"),  nullable=False)
    department_id        = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    allocated_by_id      = Column(UUID(as_uuid=True), ForeignKey("users.id"),  nullable=True)   # who performed the allocation
    allocated_at         = Column(DateTime(timezone=True), nullable=True)                        # filled on creation
    expected_return_date = Column(Date, nullable=True)
    actual_return_date   = Column(DateTime(timezone=True), nullable=True)
    return_condition     = Column(String(100), nullable=True)
    return_notes         = Column(Text, nullable=True)
    is_active            = Column(Boolean, default=True, nullable=False)

    # Relationships
    asset       = relationship("Asset",      foreign_keys=[asset_id],        back_populates="allocations")
    employee    = relationship("User",       foreign_keys=[employee_id])
    department  = relationship("Department", foreign_keys=[department_id])
    allocated_by = relationship("User",      foreign_keys=[allocated_by_id])
