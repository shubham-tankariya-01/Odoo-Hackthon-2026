from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class AuditFinding(BaseModel):
    __tablename__ = "audit_findings"

    audit_cycle_id = Column(UUID(as_uuid=True), ForeignKey("audit_cycles.id"), nullable=False)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    status = Column(String, default="pending", nullable=False)
    notes = Column(String, nullable=True)
