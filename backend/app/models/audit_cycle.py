from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class AuditCycle(BaseModel):
    __tablename__ = "audit_cycles"
    
    scope_department_id = Column(UUID(as_uuid=True), ForeignKey('departments.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)
    auditor_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    
    department = relationship("Department")
