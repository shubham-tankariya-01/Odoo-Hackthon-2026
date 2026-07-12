from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class AssetCategory(BaseModel):
    __tablename__ = "asset_categories"

    name         = Column(String, unique=True, index=True, nullable=False)
    description  = Column(String, nullable=True)
    field_schema = Column(JSONB, default=dict, nullable=False)

    assets = relationship("Asset", back_populates="category")

