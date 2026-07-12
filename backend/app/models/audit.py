from sqlalchemy import Column, String, Date, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class AuditCycle(BaseModel):
    __tablename__ = "audit_cycles"

    name = Column(String, nullable=False)
    scope_department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String, default="open", nullable=False)
    auditor_ids = Column(ARRAY(UUID(as_uuid=True)), default=[], nullable=False)

    findings = relationship("AuditFinding", back_populates="cycle", cascade="all, delete")

class AuditFinding(BaseModel):
    __tablename__ = "audit_findings"

    audit_cycle_id = Column(UUID(as_uuid=True), ForeignKey("audit_cycles.id"), nullable=False)
    asset_id = Column(UUID(as_uuid=True), nullable=True) 
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    status = Column(String, default="pending", nullable=False)
    notes = Column(String, nullable=True)

    cycle = relationship("AuditCycle", back_populates="findings")
