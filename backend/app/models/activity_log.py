from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class ActivityLog(BaseModel):
    __tablename__ = "activity_logs"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)
    target_id = Column(UUID(as_uuid=True), nullable=True)
    details = Column(String, nullable=True)
