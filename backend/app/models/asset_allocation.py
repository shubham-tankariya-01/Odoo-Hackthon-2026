from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class AssetAllocation(BaseModel):
    __tablename__ = "asset_allocations"

    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    allocated_at = Column(DateTime(timezone=True), nullable=False)
    returned_at = Column(DateTime(timezone=True), nullable=True)
