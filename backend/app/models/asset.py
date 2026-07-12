from enum import Enum
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class AssetStatus(str, Enum):
    available = "available"
    allocated = "allocated"
    reserved = "reserved"
    under_maintenance = "under_maintenance"
    lost = "lost"
    retired = "retired"
    disposed = "disposed"


# State machine: valid next statuses for each current status
ALLOWED_TRANSITIONS: dict = {
    AssetStatus.available: {
        AssetStatus.allocated,
        AssetStatus.reserved,
        AssetStatus.under_maintenance,
        AssetStatus.lost,
        AssetStatus.retired,
        AssetStatus.disposed,
    },
    AssetStatus.allocated: {
        AssetStatus.available,
        AssetStatus.under_maintenance,
        AssetStatus.lost,
    },
    AssetStatus.reserved: {
        AssetStatus.available,
        AssetStatus.allocated,
    },
    AssetStatus.under_maintenance: {
        AssetStatus.available,
    },
    AssetStatus.lost: set(),                    # terminal
    AssetStatus.retired: {AssetStatus.disposed},
    AssetStatus.disposed: set(),                    # terminal
}


class Asset(BaseModel):
    __tablename__ = "assets"

    asset_tag = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    serial_number = Column(String(255), nullable=True, unique=True)
    category_id = Column(
        UUID(
            as_uuid=True),
        ForeignKey("asset_categories.id"),
        nullable=False)
    current_status = Column(
        String(50),
        default=AssetStatus.available,
        nullable=False)
    is_bookable = Column(Boolean, default=False, nullable=False)
    custom_fields = Column(
        JSON().with_variant(
            JSONB,
            "postgresql"),
        default=dict,
        nullable=False)

    # Relationships
    category = relationship("AssetCategory", back_populates="assets")
    allocations = relationship("Allocation", back_populates="asset")
    maintenance_requests = relationship(
        "MaintenanceRequest", back_populates="asset")
