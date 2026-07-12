from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class AssetCategory(BaseModel):
    __tablename__ = "asset_categories"

    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    field_schema = Column(
        JSON().with_variant(
            JSONB,
            "postgresql"),
        default=dict,
        nullable=False)

    assets = relationship("Asset", back_populates="category")
