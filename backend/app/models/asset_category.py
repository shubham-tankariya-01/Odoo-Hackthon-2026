from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class AssetCategory(BaseModel):
    __tablename__ = "asset_categories"

    name        = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    assets = relationship("Asset", back_populates="category")
