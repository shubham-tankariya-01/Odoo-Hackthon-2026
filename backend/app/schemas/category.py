from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID
from app.schemas.common import BaseSchema


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    field_schema: Dict[str, Any] = Field(default_factory=dict)


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    field_schema: Optional[Dict[str, Any]] = None


class CategoryResponse(BaseSchema):
    name: str
    description: Optional[str] = None
    field_schema: Dict[str, Any] = Field(default_factory=dict)
    asset_count: int = 0
