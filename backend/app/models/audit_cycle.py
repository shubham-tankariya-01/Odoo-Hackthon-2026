from sqlalchemy import Column, String, DateTime
from app.models.base import BaseModel

class AuditCycle(BaseModel):
    __tablename__ = "audit_cycles"

    name = Column(String, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="planned", nullable=False)
