from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class ActivityLog(BaseModel):
    __tablename__ = 'activity_logs'
    employee_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    action      = Column(String(100), nullable=False, index=True)
    module      = Column(String(50),  nullable=False, index=True)
    entity_id   = Column(UUID(as_uuid=True), nullable=True)
    entity_type = Column(String(50),  nullable=True)
    details     = Column(JSONB, default=dict, nullable=False)
    employee = relationship('User', foreign_keys=[employee_id])
