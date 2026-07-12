from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class AuditFinding(BaseModel):
    __tablename__ = "audit_findings"
    
    audit_cycle_id = Column(UUID(as_uuid=True), ForeignKey('audit_cycles.id'), nullable=False)
    asset_id = Column(UUID(as_uuid=True), ForeignKey('assets.id'), nullable=False)
    auditor_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    finding = Column(String, nullable=False)
    
    audit_cycle = relationship("AuditCycle")
    asset = relationship("Asset")
    auditor = relationship("User")
