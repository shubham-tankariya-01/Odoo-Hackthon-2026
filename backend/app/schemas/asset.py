from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from app.schemas.common import BaseSchema
from app.models.asset import AssetStatus


class AssetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    serial_number: Optional[str] = Field(None, max_length=255)
    category_id: UUID
    is_bookable: bool = False
    custom_fields: Dict[str, Any] = Field(default_factory=dict)


class AssetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    serial_number: Optional[str] = None
    category_id: Optional[UUID] = None
    is_bookable: Optional[bool] = None
    custom_fields: Optional[Dict[str, Any]] = None


class AssetStatusUpdate(BaseModel):
    status: AssetStatus
    reason: Optional[str] = None


class AssetResponse(BaseSchema):
    asset_tag: str
    name: str
    serial_number: Optional[str] = None
    category_id: UUID
    current_status: AssetStatus
    is_bookable: bool
    custom_fields: Dict[str, Any]
