from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class ActivityLog(BaseModel):
    __tablename__ = "activity_logs"

    actor_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    recipient_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
