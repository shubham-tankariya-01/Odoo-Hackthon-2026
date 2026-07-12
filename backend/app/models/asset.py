from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class Asset(BaseModel):
    __tablename__ = "assets"

    name = Column(String, index=True, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("asset_categories.id"), nullable=True)
    status = Column(String, default="available", nullable=False)
