from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class MaintenanceRequest(BaseModel):
    __tablename__ = "maintenance_requests"

    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    requester_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, default="open", nullable=False)
